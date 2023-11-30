# Inicia servidor con: uvicorn main:app --reload
# Detener el server: Ctrl + C

# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
from routers import products, users
 
app = FastAPI()

# ROUTERS
# Nos sirven para relacionar o enrutar distintas partes de la API.
# Esto con el objetivo de separar en diferentes files las features de la API. Clean code.

app.include_router(products.router)

app.include_router(users.router)

# URL local: http://127.0.0.1:8000
@app.get("/")
async def root():
    return "¡Hola FastAPI!"

#URL local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return { "url" : "https://mouredev.com/python" }


