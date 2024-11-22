from pyannote.audio import Pipeline
from openai import OpenAI
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def verify_environment():
    """Verifica que todas las variables de entorno necesarias estén configuradas"""
    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN")
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")

def transcribe_with_openai(audio_path):
    """Transcribe el audio usando la API de Whisper de OpenAI"""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"No se encontró el archivo de audio: {audio_path}")
        
    try:
        print("Iniciando transcripción con Whisper API...")
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error en la transcripción: {e}")
        raise

def get_diarization(audio_path):
    """Obtiene la diarización del audio usando pyannote"""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"No se encontró el archivo de audio: {audio_path}")
        
    try:
        print("Iniciando diarización...")
        # Verificar el token de HuggingFace
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not hf_token:
            raise ValueError("No se encontró el token de HuggingFace en las variables de entorno")
            
        # Intentar cargar el pipeline
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token=hf_token
        )
        
        if pipeline is None:
            raise ValueError("""
            No se pudo cargar el pipeline de diarización
            """)
        
        diarization = pipeline(audio_path)
        
        # Convertir la diarización a un formato más manejable
        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append({
                'start': turn.start,
                'end': turn.end,
                'speaker': speaker,
                'start_time': f"{int(turn.start // 60):02d}:{int(turn.start % 60):02d}",
                'end_time': f"{int(turn.end // 60):02d}:{int(turn.end % 60):02d}"
            })
        
        return speaker_segments
    
    except Exception as e:
        print(f"Error en la diarización: {str(e)}")
        print("\nPor favor, verifica que:")
        print("1. Has aceptado los términos de uso en https://huggingface.co/pyannote/speaker-diarization")
        print("2. Has aceptado los términos en https://huggingface.co/pyannote/segmentation")
        print("3. Tu token de HuggingFace es válido y está correctamente configurado")
        raise
    finally:
        if 'pipeline' in locals():
            del pipeline

def process_audio_file(audio_path, output_path):
    """Procesa el archivo de audio: transcribe y diariza"""
    try:
        # Verificar configuración
        verify_environment()
        
        # Registrar tiempo de inicio
        start_time = time.time()
        print(f"Iniciando procesamiento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Paso 1: Transcribir el audio completo
        transcription = transcribe_with_openai(audio_path)
        print("Transcripción completada")
        
        # Paso 2: Obtener la diarización
        speaker_segments = get_diarization(audio_path)
        print("Diarización completada")
        
        # Paso 3: Guardar resultados
        with open(output_path, "w", encoding='utf-8') as f:
            f.write("TRANSCRIPCIÓN Y DIARIZACIÓN DE AUDIO\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("SEGMENTOS POR HABLANTE:\n")
            f.write("-" * 30 + "\n")
            for segment in speaker_segments:
                f.write(f"[{segment['start_time']} - {segment['end_time']}] {segment['speaker']}\n")
            
            f.write("\nTRANSCRIPCIÓN COMPLETA:\n")
            f.write("-" * 30 + "\n")
            f.write(transcription)
            
            elapsed_time = time.time() - start_time
            f.write(f"\n\nTiempo de procesamiento: {elapsed_time:.2f} segundos")
        
        print(f"Proceso completado. Resultados guardados en: {output_path}")
        print(f"Tiempo total de procesamiento: {elapsed_time:.2f} segundos")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        raise

if __name__ == "__main__":
    audio_path = r"C:\Users\argui\OneDrive\Escritorio\audio.mp3"
    output_path = r"C:\Users\argui\OneDrive\Escritorio\trans.txt"
    
    try:
        process_audio_file(audio_path, output_path)
    except Exception as e:
        print("\nEl proceso no pudo completarse. Por favor, sigue los pasos de solución de problemas anteriores.")