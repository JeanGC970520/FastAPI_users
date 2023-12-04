
from pydantic import BaseModel

# Entidad User (Modelo)

class User(BaseModel):
    id: int
    username: str
    email: str