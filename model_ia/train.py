from data.load_data import load_data_ml
from model_ia.preprocess import preprocess_data, split_data
from sklearn.tree import DecisionTreeRegressor
import joblib

def train_model(X_train, y_train):

    '''
    Esta función entrena y guarda el nuevo modelo cada que la BD se actualice
    
    '''


    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    
    # Guardar el modelo
    joblib.dump(model, 'daily_model.pkl')


def daily_training():
    # Cargar el dataset
    df = load_data_ml()
    
    # Preprocesamiento
    X, y = preprocess_data(df)
    
    # Dividir datos
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Entrenar modelo
    train_model(X_train, y_train)
    print("Modelo entrenado y guardado al final del día.")


