
# Users API con MongoDB
# Levantar server de MongoDB en local: 
#       ./mongod --dbpath "/home/jean/Documents/backend/MongoDB/data/"
#   Nota: Se debe posicionar en el path: /home/jean/Documents/backend/MongoDB/bin

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import dbClient
from db.schemas.user import userSchema, usersSchema
from bson import ObjectId

router = APIRouter(
    prefix="/userdb", 
    tags=["UsersDB"],                              # * Los tags nos sirven para "etiquetar"(agreupar) el router y sus operaciones, Ver docs.
    responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}} # * Agrega posibles respuestas custom.
)

# Simulando que es una DB.
usersFakeDB = []

@router.get("/", response_model=list[User])
async def users():
    return usersSchema(dbClient.local.users.find())

# Usando Path parameters. Se usan cuando un parametro es obligatorio
@router.get("/{id}")
async def userById(id: str):
    return searchUser("_id", ObjectId(id))
    
# Usando Query parameters. Se uasan cuando los parametros pueden ser opcionales, como la paginacion
@router.get("/query/") # ! Le tuve que dar otro path porque sino como la de users() tenia el mismo, ejecutava esta y no la del query
async def userQuery(id: str):
    print("Query operation")
    return searchUser("_id", ObjectId(id))

# * Nota: Se suelen usar Path parameters cuando dicho parametro es necesario para hacer la consulta.
# *       En cambio se usan los Query parameters cuando no es necesario para hacer la consulta.

# POST
# Returning 201 HTTP code when all gone fine
# Tambien podemos indicar que tipo de respuesta es la que se espera devuelva cuando todo va bien.
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED) 
async def createUser(user: User):
    if type(searchUser("email", user.email)) == User:
        # ! Cuando algo va mal es mas comun regresar un status code. En este caso con HTTPException y raise.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exist")

    # Insertando User en DB
    userDict = dict(user)
    del userDict["id"]      # Borrando campo "id" para que MongoDB lo incerte
    _id = dbClient.local.users.insert_one(userDict).inserted_id
    # Consulando usuario que acabamos de insertar. El campo de identificacion unica en MongoDB, se llama "_id"
    newUser = dbClient.local.users.find_one({"_id": _id})   # newUser es un objeto de base de datos

    newUser = userSchema(newUser)

    return User(**newUser)

# PUT
@router.put("/", response_model=User, )
async def updateUser(user: User):
    
    userDict = dict(user)
    del userDict["id"]

    try:
        dbClient.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, userDict)
    except:
        return {"error": "The user has not been updated"}

    return searchUser("_id", ObjectId(user.id))

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str):

    found = dbClient.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "Not found. The user has not been deleted"}
    
def searchUser(field: str, key):
    try:
        user = dbClient.local.users.find_one({field: key}) 
        return User(**userSchema(user))
    except:
        return {"error": "Not Found"}