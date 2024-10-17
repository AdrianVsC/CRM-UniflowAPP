"""
Este módulo tiene el objetivo de Cargar la data necesaria desde Supabase a un Dataframe
para posteriormente entrenar, testear y utilizar el modelo de Machine Learning

"""
#Importamos los módulos y librerías necesarias
from config.db import get_supabase_client
import pandas as pd

def load_data_ml():
    supabase = get_supabase_client()
    data1 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term','probability_of_conversion').execute() #Agregar cantidad de unidades
    data2 = supabase.table('customers').select('id', 'gender', 'age','country','province','city','prospect_status').execute()
    data_f = pd.merge(pd.DataFrame(data1.data), pd.DataFrame(data2.data), on='id')
    return pd.DataFrame(data_f)

def load_data_gpt():
    supabase = get_supabase_client()
    data1 = supabase.table('customer_notes').select('content_note').execute()
    data2 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term').execute()
    notas = pd.DataFrame(data1.data)
    caracteristicas = pd.DataFrame(data2.data)
    notas = notas.iloc[[-1]]
    caracteristicas = caracteristicas.iloc[[-1]]
    caracteristicas = caracteristicas.to_string()
    notas = notas.to_string()
    return caracteristicas, notas

def load_data_row():
    data = load_data_ml()
    data = data.iloc[[-1]]
    return data

def load_data_analisis(tabla: str)-> pd.DataFrame:
    supabase = get_supabase_client()
    response = supabase.table(tabla).select("*").execute()
    return pd.DataFrame(response.data)
