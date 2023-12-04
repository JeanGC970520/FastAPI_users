
from pydantic import BaseModel

# Entidad User (Modelo)

class User(BaseModel):
    # ! IMPORTANTE: Tuve que igualarlo a None por defecto 
    # ! porque si no me pedia en el requeste el campo "id"
    id: str | None = None 
    username: str
    email: str