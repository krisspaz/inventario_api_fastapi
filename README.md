# 📦 API de Inventario con FastAPI

Una API RESTful desarrollada con **FastAPI** para la gestión de inventario.  
Permite crear, listar, actualizar y eliminar productos, además de exportar el inventario a un archivo Excel.  

Ideal como ejemplo de proyecto **Back-end Developer (Python)** para portafolio.

---

## 🚀 Funcionalidades
- **CRUD de productos** (Crear, Leer, Actualizar, Eliminar).  
- **Exportación de inventario a Excel** con Pandas y OpenPyXL.  
- **Documentación automática** con Swagger UI y Redoc.  
- **Validación de datos** con Pydantic.  
- Base de datos **SQLite** (puede cambiarse fácilmente a PostgreSQL/MySQL).  

---

## 🛠️ Tecnologías usadas
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Uvicorn](https://www.uvicorn.org/)  
- [SQLAlchemy](https://www.sqlalchemy.org/)  
- [Pandas](https://pandas.pydata.org/)  
- [OpenPyXL](https://openpyxl.readthedocs.io/)  

---

## 📂 Estructura del proyecto
inventario_api/
│── main.py # Rutas principales de la API
│── database.py # Configuración de la base de datos
│── models.py # Modelos Pydantic
│── inventario.db # Base de datos SQLite
│── requirements.txt # Dependencias
│── README.md # Documentación del proyecto


## 📸 Capturas

### Swagger UI
![Swagger UI](./screenshots/swagger_ui.png)

### Crear producto
![POST Producto](./screenshots/post_producto.png)

### Listar productos
![GET Productos](./screenshots/get_productos.png)

### Exportación a Excel
![Excel Export](./screenshots/excel_export.png)
