#Importamos las dependencias que usaremos

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

#Importamos nuestros módulos
from data.load_data import load_data_ml

#Cargamos los datos
data = load_data_ml()

def preprocess_data(data):

    #Clasificamos las columnas
    categorical_cols = ['customer_interest', 'obstacles', 'customer_reaction',
                        'decision_term', 'gender', 'country', 'province', 'city', 'prospect_status']

    #Tratamiento de variables categóricas      
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    df_encoded = pd.DataFrame(ohe.fit_transform(data[categorical_cols]))
    df_encoded.columns = ohe.get_feature_names_out(categorical_cols)

    # Reemplazar columnas categóricas por las codificadas
    df = df.drop(categorical_cols, axis=1)
    df = pd.concat([df, df_encoded], axis=1)

    # Dividir en X e y (características y etiqueta)
    X = df.drop('probability_of_conversion', axis=1)
    y = df['probability_of_conversion']

    return X, y


# Dividir datos en conjunto de entrenamiento y prueba
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test




