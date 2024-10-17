from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os
from data.load_data import load_data_gpt

load_dotenv() #Cargamos las variables de entorno

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") #Cargamos la llave 

client = OpenAI(api_key=OPENAI_API_KEY) 

def generate_guidance():

    '''
    Esta función retorna la guía de OpenIA sobre cómo actuar con el cliente 
    según la última fila subida a la base
    de datos
    
    '''

    #Cargar datos
    caracteristicas, notas = load_data_gpt()

    prompt = f"""
    Eres un asistente de ventas especializado en CRM para administración de condominios. 
    Basado en los siguientes datos de prospecto:

    Características del cliente:
    {caracteristicas}

    Notas del vendedor:
    {notas}
    
    ¿Qué estrategia recomendarías para maximizar la probabilidad de conversión de este cliente?
    """

    response = client.chat.completions.create(

        model="gpt-4o-mini-2024-07-18",  # Usa el modelo adecuado
        messages=[
            {"role": "system", "content": "Eres un asistente de ventas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )

    respuesta = response.choices[0].message.content.strip()

    return respuesta



