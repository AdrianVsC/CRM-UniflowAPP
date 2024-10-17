import joblib
import pandas as pd
from data.load_data import load_data_row
from model_ia.preprocess import preprocess_data

# Función para predecir la probabilidad de conversión
def predict_conversion():

    prospect_row = load_data_row()    
    
    # Cargar el modelo entrenado
    model = joblib.load('daily_model.pkl')

    # Preprocesar la fila del prospecto
    # Si necesitas transformar las columnas categóricas a OneHotEncoded, lo haces aquí
    prospect_row_encoded = preprocess_data(prospect_row)

    # Hacer la predicción
    probability = model.predict(prospect_row_encoded)

    return probability[0]
