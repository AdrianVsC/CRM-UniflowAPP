from model_ia.train import daily_training
import schedule
import time

# Configuración de schedule para ejecutar a las 11:59 PM cada día
schedule.every().day.at("23:59").do(daily_training)

while True:
    schedule.run_pending()
    time.sleep(60)