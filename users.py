# Inicia servidor con: uvicorn users:app --reload
# Detener el server: Ctrl + C

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int 

# Simulando que es una DB.
usersFakeDB = [ User(id= 1,name="Jean", surname="Garcia", url="https://jeangacia.com", age=26),
                User(id= 2,name="James", surname="Garcia", url="https://jamesgacia.com", age=16),
                User(id= 3,name="Alfredo", surname="Garcia", url="https://alfredogacia.com", age=58),]

@app.get("/usersjson")
async def usersJson():
    return [{"name" : "Jean", "surname" : "Garcia", "url" : "https://jeangacia.com", "age" : 26},
            {"name" : "James", "surname" : "Garcia", "url" : "https://jamesgacia.com", "age" : 16},
            {"name" : "Alfredo", "surname" : "Garcia", "url" : "https://alfredogacia.com", "age" : 58},]


@app.get("/usersclass")
async def usersClass():
    return User(name="Jean", surname="Garcia", url="https://jeangacia.com", age=26)

@app.get("/users")
async def users():
    return usersFakeDB

# Usando Path parameters.
@app.get("/user/{id}")
async def userById(id: int):
    return searchUser(id)
    
# Usando Query parameters.
@app.get("/userquery/")
async def userQuery(id: int):
    return searchUser(id)
    
def searchUser(id: int):
    users = filter(lambda user: user.id == id, usersFakeDB)
    try:
        return list(users)[0] 
    except:
        return {"error": "Not Found"}