from fastapi import APIRouter

# * IMPORTANTE: Cuando se usa un ROUTER, es muy habitual usar la misma base del path. 
# * en este caso: "/products". Con el parametro prefix, se le puede indicar al 
# * ROUTER este path. Con lo cual ya todas las operaciones, tendran como base ese path.

router = APIRouter(
    prefix="/products", 
    tags=["Products"],                          # * Los tags nos sirven para "etiquetar"(agreupar) el router y sus operaciones, Ver docs.
    responses={404 : {"message": "No encontrado"}} # * Agrega posibles respuestas custom.
)

productsFakeDB = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def products():
    return productsFakeDB

@router.get("/{id}")
async def products(id: int):
    return productsFakeDB[id]