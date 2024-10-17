import joblib
import pandas as pd
from data.load_data import load_data_row
from model_ia.preprocess import preprocess_data

def predict_conversion():

    '''
    Esta función es la que retornará la predicción según la última fila que se ingresó
    a la base de datos

    '''

    prospect_row = load_data_row()    
    
    # Cargar el modelo entrenado
    model = joblib.load('daily_model.pkl')

    # Preprocesar la fila del prospecto
    prospect_row_encoded = preprocess_data(prospect_row)

    # Hacer la predicción
    probability = model.predict(prospect_row_encoded)

    return probability[0]
