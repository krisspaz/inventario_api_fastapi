from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from database import SessionLocal, Producto
from models import ProductoCreate, ProductoResponse

app = FastAPI(title="API de Inventario")

# Dependencia para sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado"}

@app.get("/exportar/")
def exportar_excel(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    if not productos:
        return {"message": "No hay productos para exportar"}
    data = [{"id": p.id, "nombre": p.nombre, "cantidad": p.cantidad, "precio": p.precio} for p in productos]
    df = pd.DataFrame(data)
    archivo = "inventario.xlsx"
    df.to_excel(archivo, index=False)
    return {"message": f"Inventario exportado a {archivo}"}
