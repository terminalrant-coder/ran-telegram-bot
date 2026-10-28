import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/healthz")
def health_check():
    return {"status": "RANT bot is online!"}

# Aquí abajo puedes mantener o agregar la lógica de tu bot de Telegram si la tienes
