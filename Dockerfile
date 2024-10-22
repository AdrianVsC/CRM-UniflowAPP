# Utiliza una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copia todo el contenido del directorio actual al contenedor
COPY . .

# Expone el puerto 8000 (FastAPI usa 8000 por defecto)
EXPOSE 8000

# Comando para ejecutar tu aplicación FastAPI con Uvicorn
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]