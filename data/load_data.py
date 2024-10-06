"""
Este módulo tiene el objetivo de Cargar la data necesaria desde Supabase a un Dataframe
para posteriormente entrenar, testear y utilizar el modelo de Machine Learning

"""

#Importamos los módulos y librerías necesarias
from config.db import get_supabase_client
import pandas as pd

def load_data():
    supabase = get_supabase_client()
    data = supabase.table('customers').select('country','state','province','city').execute()
    return pd.DataFrame(data.data)
data = load_data()
print(data)