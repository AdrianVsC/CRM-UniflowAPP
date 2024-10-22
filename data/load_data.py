# """
# Este módulo tiene el objetivo de Cargar la data necesaria desde Supabase a un Dataframe
# para posteriormente entrenar, testear y utilizar el modelo de Machine Learning

# """
# #Importamos los módulos y librerías necesarias
# from config.db import get_supabase_client
# import pandas as pd

# def load_data_ml():
#     supabase = get_supabase_client()
#     data1 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term','probability_of_conversion').execute() #Agregar cantidad de unidades
#     data2 = supabase.table('customers').select('id', 'gender', 'age','country','province','city','prospect_status').execute()
#     data_f = pd.merge(pd.DataFrame(data1.data), pd.DataFrame(data2.data), on='id')
    
   
#     return pd.DataFrame(data_f)

# def load_data_gpt():
#     supabase = get_supabase_client()
#     data1 = supabase.table('customer_notes').select('content_note').execute()
#     data2 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term').execute()
#     notas = pd.DataFrame(data1.data)
#     caracteristicas = pd.DataFrame(data2.data)
#     notas = notas.iloc[[-1]]
#     caracteristicas = caracteristicas.iloc[[-1]]
#     caracteristicas = caracteristicas.to_string()
#     notas = notas.to_string()
#     return caracteristicas, notas

# def load_data_row():
#     data = load_data_ml()
#     data = data.iloc[[-1]]
#     return data

"""
Este módulo tiene el objetivo de Cargar la data necesaria desde Supabase a un Dataframe
para posteriormente entrenar, testear y utilizar el modelo de Machine Learning
"""

# Importamos los módulos y librerías necesarias
from config.db import get_supabase_client
import pandas as pd

def load_data_ml():
    supabase = get_supabase_client()
    
    # Obtenemos los datos de las tablas
    data1 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term','probability_of_conversion').execute() 
    data2 = supabase.table('customers').select('id', 'gender', 'age','country','province','city','prospect_status').execute()
    
    # Convertimos los datos en DataFrames
    df1 = pd.DataFrame(data1.data)
    df2 = pd.DataFrame(data2.data)
    
    # Validación de que ambas tablas tienen datos
    if df1.empty or df2.empty:
        return "Error: No hay datos suficientes en las tablas para realizar el merge."

    # Validación de que ambas tablas tienen la columna 'id'
    if 'id' not in df1.columns or 'id' not in df2.columns:
        return "Error: La columna 'id' no está presente en una de las tablas."
    
    # Realizamos el merge
    data_f = pd.merge(df1, df2, on='id')
    
    return pd.DataFrame(data_f)

def load_data_gpt():
    supabase = get_supabase_client()

    # Obtenemos los datos de las tablas
    data1 = supabase.table('customer_notes').select('content_note').execute()
    data2 = supabase.table('customer_notes').select('id','customer_interest','obstacles','customer_reaction','competition', 'decision_term').execute()

    # Convertimos los datos en DataFrames
    notas = pd.DataFrame(data1.data)
    caracteristicas = pd.DataFrame(data2.data)

    # Validación de que ambas tablas tienen datos
    if notas.empty or caracteristicas.empty:
        return "Error: No hay datos suficientes para generar la guía GPT."

    # Obtenemos la última fila
    notas = notas.iloc[[-1]]
    caracteristicas = caracteristicas.iloc[[-1]]

    # Convertimos los datos a string
    caracteristicas = caracteristicas.to_string()
    notas = notas.to_string()

    return caracteristicas, notas

def load_data_row():
    data = load_data_ml()
    
    # Validación de que se cargaron datos correctamente
    if isinstance(data, str):  # Si la función devolvió un error como string
        return data

    # Obtenemos la última fila de datos
    data = data.iloc[[-1]]


    return data

