from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Importación de Rutas Anteriores y Nuevas
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router

# Importación del Middleware Personalizado de Trazabilidad
from app.middlewares.request_middleware import RequestTracingMiddleware

# Configuración del Limitador de Peticiones (Rate Limiting)
limiter = Limiter(key_func=get_remote_address)

# Fase 12: Configuración de Metadatos Avanzados para Swagger/OpenAPI v3.0.0
app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0"
)

# Configurar el manejador global para cuando un cliente exceda el límite (Error 429)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── 1. MIDDLEWARE PERSONALIZADO (Trazabilidad y Cabeceras - Fase 10) ──
app.add_middleware(RequestTracingMiddleware)

# ── 2. CONFIGURACIÓN DE CORS (Fase 9 - Orígenes Autorizados) ──
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 3. REGISTRO E INCLUSIÓN DE ROUTERS ──
# Agregamos el nuevo módulo de autenticación primero
app.include_router(auth_router)

# Tus routers de la versión anterior
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido papi – Capa de seguridad v3.0.0 Activa"}