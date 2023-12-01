
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext 
from datetime import datetime, timedelta


ALGORITHM = "HS256"         # Algoritmo de incriptacion para JWT
ACCESS_TOKEN_DURATION = 1   # El Token seria valido por un tiempo de un minuto
# Clave de encriptacion, semilla. Esto hace muy seguro el token ya que esta KEY_SECRET, solo la conoce el Backend
SECRET = "2c18e6da13c483c3e2707327c5a183e691a9a2734588fd2a54a2c979365b17d6A"

app = FastAPI()

# tockenUrl es el URL de donde se obtendra el OAuht2 token
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Contexto de incriptacion
crypt = CryptContext(schemes=["bcrypt"])

# Models
class User(BaseModel):
    username: str
    fullName: str
    emial: str
    disabled: bool

class UserDB(User):
    password: str

# DB con contraseñas encriptadas con "bcrypt" scheme 
usersDBFake = {
    "jeandev" : {
        "username"  : "jeandev",
        "fullName"  : "Jean Pool Garcia",
        "emial"     : "j.jjjean@hotmail.es",
        "disabled"  : False,
        "password"  : "$2a$12$Efa8sHJsdT/Gw0tNRQ2pJOcp3sDn1G4OFBUthu0cRsorb4SofDtjG",
    },
    "jeandev2" : {
        "username"  : "jeandev2",
        "fullName"  : "Jean Pool Garcia 2",
        "emial"     : "j.jjjean2@hotmail.es",
        "disabled"  : True,
        "password"  : "$2a$12$VE.zneuoa9Bab95q4d.9eOFEfty6YSiwUzN49X15LrjHJqphn3j2i",
    },
} 

def searchUserDB(username: str):
    if username in usersDBFake:
        # ! IMPORTANTE: ** esto significa que estamos desenpaquetando un diccionario
        return UserDB(**usersDBFake[username])
    
def searchUser(username: str):
    if username in usersDBFake:
        # ! IMPORTANTE: ** esto significa que estamos desenpaquetando un diccionario
        return User(**usersDBFake[username])

async def authUser(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate" : "Bearer"}
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ ALGORITHM ]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return searchUser(username)

# DEPENDENCY
async def currentUser(user: User = Depends(authUser)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo",
        )
    return user

# * Con Depends() significa que esta operacion va a recibir datos pero NO depende de nadie
# * Si a Depends(criterio) le pasamos un criterio, entonces va a depender de ese criterio.
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userDB = usersDBFake.get(form.username)
    if not userDB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = searchUserDB(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcto")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    # ! Al hacer esta estructura de datos, JWT puede verificar si el Token ya expiro.
    accessToken = {
        "sub" : user.username,
        "exp" : expire,
    } 
    # ! IMPORTANTE: Se pasa un token incriptado que solo conozca el backend. 
    return {"acces_token" : jwt.encode(accessToken, SECRET, algorithm=ALGORITHM), "token_type": "bearer" }

# * Depends() en este caso hace que tengamos un User si currentUser termina bien. Depende de currentUser 
# ! IMPORTANTE: En este caso estamos usando dependencias y sub-dependencias. 
# !     -- Explicacion: Al depender de currentUser(), primero se debe resover lo que hay dentro 
# !             de ese metodo. Pero como a su vez éste deoende de authUser(), debe resolver ese
# !             otro metodo antes. Éste a su vez depende de oauth2.
@app.get("/users/me")
async def me(user: User = Depends(currentUser)):
    return user


