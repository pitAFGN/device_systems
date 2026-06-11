from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes import user_routes

# LÓGICA ORM: Crea las tablas físicas en el archivo .db al arrancar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="Evolución de la API con persistencia de datos usando SQLAlchemy y SQLite.",
    version="2.0.0"
)

# Registra las rutas automatizadas conectadas a la base de datos
app.include_router(user_routes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a la versión persistente de device_systems API"}