
"""
main.py
---------
API principal para la gestión de inventario usando FastAPI.
Incluye endpoints CRUD y exportación a Excel.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from typing import Generator, List

from database import SessionLocal, Producto
from models import ProductoCreate, ProductoResponse

app = FastAPI(
    title="API de Inventario",
    description="API RESTful para la gestión de productos de inventario.",
    version="1.0.0"
)

def get_db() -> Generator[Session, None, None]:
    """
    Provee una sesión de base de datos para cada request.
    Cierra la sesión automáticamente al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)) -> ProductoResponse:
    """
    Crea un nuevo producto en el inventario.
    """
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/", response_model=List[ProductoResponse], tags=["Productos"])
def listar_productos(db: Session = Depends(get_db)) -> List[ProductoResponse]:
    """
    Lista todos los productos del inventario.
    """
    productos = db.query(Producto).all()
    # Convertir a ProductoResponse para cumplir con el tipado
    return [ProductoResponse.model_validate(p) for p in productos]

@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)) -> ProductoResponse:
    """
    Actualiza los datos de un producto existente.
    """
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    for key, value in producto.model_dump().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)) -> None:
    """
    Elimina un producto del inventario.
    """
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return

@app.get("/exportar/", tags=["Utilidades"])
def exportar_excel(db: Session = Depends(get_db)):
    """
    Exporta el inventario a un archivo Excel (inventario.xlsx).
    """
    productos = db.query(Producto).all()
    if not productos:
        return {"message": "No hay productos para exportar"}
    # Acceso seguro a los atributos, evitando Column
    data = []
    for p in productos:
        # Extraer valores primitivos usando __dict__ para evitar Column
        row = {
            "id": p.__dict__.get("id", 0),
            "nombre": p.__dict__.get("nombre", ""),
            "cantidad": p.__dict__.get("cantidad", 0),
            "precio": p.__dict__.get("precio", 0.0)
        }
        data.append(row)
    df = pd.DataFrame(data)
    archivo = "inventario.xlsx"
    df.to_excel(archivo, index=False)
    return {"message": f"Inventario exportado a {archivo}"}
