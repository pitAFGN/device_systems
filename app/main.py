from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes import user_routes
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# LÓGICA ORM: Crea las tablas físicas en el archivo .db al arrancar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="Evolución de la API con persistencia de datos usando SQLAlchemy y SQLite.",
    version="2.0.0"
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

# Registra las rutas automatizadas conectadas a la base de datos
app.include_router(user_routes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido papi"}