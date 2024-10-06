"""
En este módulo configuramos la conexión con la base de datos de Supabase.
Definimos la función get_supabase_client() 
esto con el objetivo de facilitar la creación del cliente

"""

#Importamos las librerías necesarias
import os
from supabase import create_client
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Variables de conexión a Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificar que las variables de entorno estén presentes
if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError("Faltan las variables de entorno: SUPABASE_URL y/o SUPABASE_KEY")

# Crear cliente de Supabase al inicio
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    """Devuelve el cliente de Supabase ya creado.

    Returns:
        Client: Cliente de Supabase.
    """
    return supabase_client
