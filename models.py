
"""
models.py
---------
Modelos Pydantic para validación y serialización de datos de productos.
"""

from pydantic import BaseModel

class ProductoBase(BaseModel):
    """
    Modelo base con atributos comunes para productos.
    """
    nombre: str
    cantidad: int
    precio: float

class ProductoCreate(ProductoBase):
    """
    Modelo para creación de productos (input).
    """
    pass

class ProductoResponse(ProductoBase):
    """
    Modelo de respuesta con ID (output).
    """
    id: int

    class Config:
        orm_mode = True
