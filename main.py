# Inicia servidor con: uvicorp main:app --reload
# Detener el server: Ctrl + C

# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI

app = FastAPI()

# URL local: http://127.0.0.1:8000
@app.get("/")
async def root():
    return "¡Hola FastAPI!"

#URL local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return { "url" : "https://mouredev.com/python" }


