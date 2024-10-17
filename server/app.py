from fastapi import FastAPI
from pydantic import BaseModel
from model_ia.predict import predict_conversion
from model_ia.openia import generate_guidance
from model_ia.train import daily_training
from data.load_data import load_data_ml

app = FastAPI(
    title="API de Modelo IA y Data",
    description="Acá vamos a probar las rutas para ver si andan bien.",
    version="0.1.0",
    contact={
        "name": "ElJonpi",
        "email": "ignacio@uniflowapp.com"
    }
)


@app.get("/")
def read_root():
    return {"message":"Servidor Arriba hijo de tu puta madre"}

# Modelo de datos para la solicitud de predicción
class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    # Añade más características según tu modelo de predicción

# Ruta para obtener una predicción de conversión
@app.post("/predict")
async def predict_endpoint(request: PredictionRequest):
    probability = predict_conversion()
    return {"prediction_probability": probability}

# Ruta para obtener guía de ventas generada por OpenAI
@app.get("/guidance")
async def guidance_endpoint():
    guidance = generate_guidance()
    return {"guidance": guidance}

# Ruta para ejecutar el entrenamiento diario del modelo
@app.post("/train")
async def train_endpoint():
    daily_training()
    return {"message": "Modelo entrenado y guardado"}

# Ruta para cargar y devolver los datos de la base
@app.get("/data")
async def data_endpoint():
    data = load_data_ml()
    return {"data": data.to_json(orient='records')}

# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)