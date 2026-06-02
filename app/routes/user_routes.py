from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdateFull, UserUpdatePartial
from app.services.user_service import UserService
from app.dependencies.user_dependencies import get_valid_user_or_404, verify_email_uniqueness
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna una lista con todos los usuarios registrados, permitiendo filtrar por rol y/o estado activo."
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, user, support)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    return UserService.get_all_users(role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Busca y retorna la información detallada de un usuario específico usando su ID."
)
def get_user_by_id(user: dict = Depends(get_valid_user_or_404)):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Registra un usuario en el sistema. Valida que el email ingresado sea único."
)
def create_user(user_in: UserCreate):
    verify_email_uniqueness(user_in.email)
    return UserService.create_user(user_in)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa de usuario (PUT)",
    description="Reemplaza todos los datos de un usuario existente. Valida que el email no pertenezca a otro usuario."
)
def update_user_complete(
    user_in: UserUpdateFull,
    current_user: dict = Depends(get_valid_user_or_404)
):
    verify_email_uniqueness(user_in.email, current_user_id=current_user["id"])
    return UserService.update_user_full(current_user["id"], user_in)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de usuario (PATCH)",
    description="Modifica uno o múltiples campos específicos de un usuario. Lanza un error 400 si el cuerpo del JSON está vacío."
)
def update_user_partial(
    user_in: UserUpdatePartial,
    current_user: dict = Depends(get_valid_user_or_404)
):
    # Validar si el cliente envió un body sin atributos utilizables
    payload_data = user_in.model_dump(exclude_unset=True)
    if not payload_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar"
        )
    
    if "email" in payload_data:
        verify_email_uniqueness(payload_data["email"], current_user_id=current_user["id"])
        
    return UserService.update_user_partial(current_user["id"], user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (DELETE)",
    description="Remueve un usuario del sistema permanentemente por su ID. Retorna Código 204 No Content si es exitoso."
)
def delete_user(current_user: dict = Depends(get_valid_user_or_404)):
    UserService.delete_user(current_user["id"])
    return None # Al usar 204, no se retorna cuerpo