from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess

# Cargar variables de entorno
load_dotenv()

# Configurar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

path1 = r"C:\Users\argui\OneDrive\Escritorio\audio.mp3"
# if path[-3:] != 'wav':
#     subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
#     path = 'audio.wav'

audio_file = open(path1, "rb")
transcript = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["segment"]
)



# print(transcript.words)

# for segment in transcript.segments:
#     print(f"Speaker1: {segment.text}")

# Supongamos que 'transcript' es el objeto que obtuviste de la API de OpenAI
# y tiene la estructura de tipo TranscriptionVerbose.

# Convertir la transcripción a un diccionario
# transcript_dict = {
#     'segments': []
# }

# # Iteramos sobre cada segmento en la transcripción
# Supongamos que 'transcript' es el objeto que obtuviste de la API de OpenAI
# y tiene la estructura de tipo TranscriptionVerbose.

# Convertir la transcripción a una lista de diccionarios
transcript_dict = []

# Iteramos sobre cada segmento en la transcripción
for i, segment in enumerate(transcript.segments):
    segment_dict = {
        'id': i,  # Usamos el índice como ID
        'seek': 0,  # Valor fijo para seek
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

# Ahora puedes imprimir el diccionario resultante
print(transcript_dict)

