
"""
database.py
------------
Configuración de la base de datos y modelo SQLAlchemy para productos.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./inventario.db"

# Crear el engine de la base de datos SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crear la sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Declarative base para modelos ORM
Base = declarative_base()

class Producto(Base):
    """
    Modelo ORM de producto para la tabla 'productos'.
    """
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)
