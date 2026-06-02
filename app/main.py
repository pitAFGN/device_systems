from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "## Sistema de Gestión de Usuarios Avanzado\n"
        "Esta API REST profesional permite la administración completa del recurso `/users` "
        "con validaciones mediante Pydantic v2, manejo estructurado de excepciones HTTP, "
        "e inyección de dependencias modulares."
    ),
    version="2.0.0",
    contact={
        "name": "Andres Felipe Gonzalez Noreña",
        "url": "https://github.com/tu-usuario",
    }
)

# Inclusión de las rutas modulares
app.include_router(user_router)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "device_systems API v2.0.0 está en ejecución. Dirígete a /docs para la documentación."}