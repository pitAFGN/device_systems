from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada en memoria
db_users = [
    {"id": 1, "name": "Andres Gonzalez", "email": "andres@device.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Maria Lopez", "email": "maria@device.com", "role": "user", "is_active": False},
    {"id": 3, "name": "Carlos Ruiz", "email": "carlos@device.com", "role": "support", "is_active": True},
]

# Función auxiliar para añadir cabeceras personalizadas obligatorias en la Fase 5
def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# --- ENDPOINTS GET ---

@router.get("", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    add_custom_headers(response)
    filtered_users = db_users

    # Aplicar filtro de rol si está presente
    if role is not None:
        filtered_users = [u for u in filtered_users if u["role"] == role.lower()]

    # Aplicar filtro de estado activo si está presente
    if is_active is not None:
        filtered_users = [u for u in filtered_users if u["is_active"] == is_active]

    return filtered_users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    add_custom_headers(response)
    
    user = next((u for u in db_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

# --- ENDPOINT POST ---

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, response: Response):
    add_custom_headers(response)

    # Validar si el correo ya existe
    email_exists = any(u["email"] == user_data.email for u in db_users)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado"
        )

    # Generar un ID autoincremental básico
    new_id = max(u["id"] for u in db_users) + 1 if db_users else 1
    
    # Construir el nuevo usuario
    new_user = {
        "id": new_id,
        **user_data.model_dump() # Convierte el modelo Pydantic v2 a diccionario
    }
    
    db_users.append(new_user)
    return new_user