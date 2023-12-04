# Inicia servidor con: uvicorn main:app --reload
# Detener el server: Ctrl + C

# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redoc

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles
 
app = FastAPI()

# ROUTERS
# Nos sirven para relacionar o enrutar distintas partes de la API.
# Esto con el objetivo de separar en diferentes files las features de la API. Clean code.

app.include_router(products.router)

app.include_router(users.router)

app.include_router(basic_auth_users.router)

app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)

# * Exponiendo recursos ESTATICOS. Tales como imagenes, PDF's, etc.
# El primer parametro, llamado path, corresponde al path raiz que se ocupara para acceder al recurso
# El segundo parametro, llamado app, es donde se encuentra el recurso a exponer. En este caso se expone todo el directorio "static"
# por ello en la ruta debemos agregar el subdirectorio "/images" para acceder a la imagen "think=twice.png"
# El tercer parametro, llamado name, es el nombre de lo que se expondra

# http://127.0.0.1:8000/static/images/think_twice.png
app.mount("/static", StaticFiles(directory="static"), "static")

# URL local: http://127.0.0.1:8000
@app.get("/")
async def root():
    return "¡Hola FastAPI!"

#URL local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return { "url" : "https://mouredev.com/python" }


