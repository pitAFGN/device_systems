import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("device_systems.middleware")

class RequestTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        
        # Generar o propagar el Request ID único
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        # Procesar la petición original
        response: Response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Inyectar las cabeceras requeridas obligatoriamente por la guía
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id
        
        # Registrar log detallado en la consola de la terminal
        logger.info(
            f"ID: {request_id} | Método: {request.method} | Ruta: {request.url.path} | "
            f"Status: {response.status_code} | Tiempo: {process_time:.4f}s"
        )
        
        return response