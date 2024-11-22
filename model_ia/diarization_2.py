import datetime
import subprocess
import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from dotenv import load_dotenv
from openai import OpenAI
import os

from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import numpy as np

# Cargar variables de entorno
load_dotenv()

# Configurar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


embedding_model = PretrainedSpeakerEmbedding( 
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu"))


path = r"C:\Users\argui\OneDrive\Escritorio\audio.mp3"

# Verificar si el archivo es mp3 y convertirlo a wav
if path[-3:] != 'wav':
    subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
    path = 'audio.wav'

num_speakers = 2  

language = 'English'  

model_size = 'large'  

model_name = model_size
if language == 'English' and model_size != 'large':
    model_name += '.en'  

audio = Audio()


def transcribe_with_openai(audio_path):
    """Transcribe el audio usando la API de Whisper de OpenAI"""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"No se encontró el archivo de audio: {audio_path}")
        
    try:
        print("Iniciando transcripción con Whisper API...")
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        return transcript.segments
    except Exception as e:
        print(f"Error en la transcripción: {e}")
        raise
    

def segment_embedding(segment):
  start = segment["start"]
  end = min(duration, segment["end"])
  clip = Segment(start, end)
  waveform, sample_rate = audio.crop(path, clip)
  return embedding_model(waveform[None])



transcript_dict = []
result = transcribe_with_openai(path)
for i, segment in enumerate(result):
    segment_dict = {
        'id': i,  
        'seek': 0,  
        'start': segment.start,
        'end': segment.end,
        'text': segment.text,
        'tokens': segment.tokens,
        'temperature': segment.temperature,
        'avg_logprob': segment.avg_logprob,
        'compression_ratio': segment.compression_ratio,
        'no_speech_prob': segment.no_speech_prob,
    }
    transcript_dict.append(segment_dict)

segments = transcript_dict

with contextlib.closing(wave.open(path,'r')) as f:
  frames = f.getnframes()
  rate = f.getframerate()
  duration = frames / float(rate)

embeddings = np.zeros(shape=(len(segments), 192))
for i, segment in enumerate(segments):
  embeddings[i] = segment_embedding(segment)

embeddings = np.nan_to_num(embeddings)

clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
labels = clustering.labels_

for i in range(len(segments)):
  segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

def time(secs):
  return datetime.timedelta(seconds=round(secs))

f = open("transcript.txt", "w")

for (i, segment) in enumerate(segments):
  if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
    f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
  f.write(segment["text"][1:] + ' ')
f.close()




