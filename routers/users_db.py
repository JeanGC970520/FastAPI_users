
# Users API con MongoDB

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import dbClient
from db.schemas.user import userSchema

router = APIRouter(
    prefix="/userdb", 
    tags=["UsersDB"],                              # * Los tags nos sirven para "etiquetar"(agreupar) el router y sus operaciones, Ver docs.
    responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}} # * Agrega posibles respuestas custom.
)

# Simulando que es una DB.
usersFakeDB = []

@router.get("/")
async def users():
    return usersFakeDB

# Usando Path parameters. Se usan cuando un parametro es obligatorio
@router.get("/{id}")
async def userById(id: int):
    return searchUser(id)
    
# Usando Query parameters. Se uasan cuando los parametros pueden ser opcionales, como la paginacion
@router.get("/")
async def userQuery(id: int):
    return searchUser(id)

# * Nota: Se suelen usar Path parameters cuando dicho parametro es necesario para hacer la consulta.
# *       En cambio se usan los Query parameters cuando no es necesario para hacer la consulta.

# POST
# Returning 201 HTTP code when all gone fine
# Tambien podemos indicar que tipo de respuesta es la que se espera devuelva cuando todo va bien.
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED) 
async def createUser(user: User):
    if type(searchUserByEmial(user.email)) == User:
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
@router.put("/")
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
@router.delete("/{id}")
async def deleteUser(id: int):
    found = False

    for index, savedUser in enumerate(usersFakeDB):
        if savedUser.id == id:
            del usersFakeDB[index]
            found = True
            break 

    if not found:
        return {"error": "Not found. The user has not been deleted"}
    
def searchUserByEmial(email: str):
    try:
        user = dbClient.local.users.find_one({"email": email}) 
        return User(**userSchema(user))
    except:
        return {"error": "Not Found"}
    
def searchUser(id: int):
    return ""