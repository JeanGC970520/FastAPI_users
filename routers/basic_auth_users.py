
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

# tockenUrl es el URL de donde se obtendra el OAuht2 token
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Models
class User(BaseModel):
    username: str
    fullName: str
    emial: str
    disabled: bool

class UserDB(User):
    password: str

# DB
usersDB = {
    "jeandev" : {
        "username"  : "jeandev",
        "fullName"  : "Jean Pool Garcia",
        "emial"     : "j.jjjean@hotmail.es",
        "disabled"  : False,
        "password"  : "123456",
    },
    "jeandev2" : {
        "username"  : "jeandev2",
        "fullName"  : "Jean Pool Garcia 2",
        "emial"     : "j.jjjean2@hotmail.es",
        "disabled"  : True,
        "password"  : "654321",
    },
} 

def searchUserDB(username: str):
    if username in usersDB:
        # ! IMPORTANTE: ** esto significa que estamos desenpaquetando un diccionario
        return UserDB(**usersDB[username])
    

def searchUser(username: str):
    if username in usersDB:
        return User(**usersDB[username])

# DEPENDENCY
async def currentUser(token: str = Depends(oauth2)):
    # * En este caso el token coincide con el nombre de usuario.
    user = searchUser(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo",
        )
    return user

# * Con Depends() significa que esta operacion va a recibir datos pero NO depende de nadie
# * Si a Depends(criterio) le pasamos un criterio, entonces va a depender de ese criterio.
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userDB = usersDB.get(form.username)
    if not userDB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = searchUserDB(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcto")
    
    # ! IMPORTANTE: Deberia pasarse un token incriptado que solo conozca el backend. 
    # Para fines practicos se pasa el username
    return {"acces_token" : user.username, "token_type": "bearer" }

# * Depends() en este caso hace que tengamos un User si currentUser termina bien. Depende de currentUser 
@router.get("/users/me")
async def me(user: User = Depends(currentUser)):
    return user