
# Users API con MongoDB

from fastapi import APIRouter, HTTPException
from db.models.user import User

router = APIRouter(
    prefix="/userdb", 
    tags=["UsersDB"],                              # * Los tags nos sirven para "etiquetar"(agreupar) el router y sus operaciones, Ver docs.
    responses={404 : {"message": "No encontrado"}} # * Agrega posibles respuestas custom.
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
@router.post("/", response_model=User, status_code=201) 
async def createUser(user: User):
    if type(searchUser(user.id)) == User:
        # ! Cuando algo va mal es mas comun regresar un status code. En este caso con HTTPException y raise.
        raise HTTPException(status_code=309, detail="User exist")

    # Insertando User en DB
    usersFakeDB.append(user)
    return user

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
    
def searchUser(id: int):
    users = filter(lambda user: user.id == id, usersFakeDB)
    try:
        return list(users)[0] 
    except:
        return {"error": "Not Found"}