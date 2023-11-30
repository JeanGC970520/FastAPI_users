# Inicia servidor con: uvicorn users:app --reload
# Detener el server: Ctrl + C

from fastapi import FastAPI, HTTPException
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

# Usando Path parameters. Se usan cuando un parametro es obligatorio
@app.get("/user/{id}")
async def userById(id: int):
    return searchUser(id)
    
# Usando Query parameters. Se uasan cuando los parametros pueden ser opcionales, como la paginacion
@app.get("/userquery/")
async def userQuery(id: int):
    return searchUser(id)

# * Nota: Se suelen usar Path parameters cuando dicho parametro es necesario para hacer la consulta.
# *       En cambio se usan los Query parameters cuando no es necesario para hacer la consulta.

# POST
# Returning 201 HTTP code when all gone fine
# Tambien podemos indicar que tipo de respuesta es la que se espera devuelva cuando todo va bien.
@app.post("/user/", response_model=User, status_code=201) 
async def createUser(user: User):
    if type(searchUser(user.id)) == User:
        # ! Cuando algo va mal es mas comun regresar un status code. En este caso con HTTPException y raise.
        raise HTTPException(status_code=309, detail="User exist")

    # Insertando User en DB
    usersFakeDB.append(user)
    return user

# PUT
@app.put("/user/")
async def updateUser(user: User):
    found = False

    for index, savedUser in enumerate(usersFakeDB):
        if savedUser.id == user.id:
            usersFakeDB[index] = user
            found = True
            break 
    
    if not found:
        return {"error": "The user has not been updated"}
    return user

# DELETE
@app.delete("/user/{id}")
async def deleteUser(id: int):
    found = False

    for index, savedUser in enumerate(usersFakeDB):
        if savedUser.id == id:
            del usersFakeDB[index]
            found = True
            break 

    if not found:
        return {"error": "Not found. The user has not been deleted"}
    
def searchUser(id: int):
    users = filter(lambda user: user.id == id, usersFakeDB)
    try:
        return list(users)[0] 
    except:
        return {"error": "Not Found"}