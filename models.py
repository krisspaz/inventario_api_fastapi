from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    class Config:
        orm_mode = True
