from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserPatch
from app.services.user_service import UserService
# IMPORTACIÓN CORREGIDA: Apunta exactamente a database_dependency
from app.dependencies.database_dependency import get_db, get_valid_user_or_404, verify_email_uniqueness
from app.models.user_model import User
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna una lista con todos los usuarios de la base de datos, permitiendo filtrar por rol y/o estado activo, y ordenar los resultados."
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    sort_by: Optional[str] = Query("name", description="Ordenar usuarios por 'name' o 'created_at'"),
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db=db, role=role, is_active=is_active, sort_by=sort_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Busca y retorna la información detallada de un usuario específico directamente desde la base de datos usando su ID."
)
def get_user_by_id(current_user: User = Depends(get_valid_user_or_404)):
    return current_user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Registra un usuario en la base de datos. Valida previamente que el email ingresado sea único."
)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    verify_email_uniqueness(email=user_in.email, db=db)
    return UserService.create_user(db=db, user_data=user_in)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa de usuario (PUT)",
    description="Reemplaza todos los datos de un usuario existente en la base de datos. Valida que el email no pertenezca a otro usuario."
)
def update_user_complete(
    user_in: UserUpdate,
    current_user: User = Depends(get_valid_user_or_404),
    db: Session = Depends(get_db)
):
    verify_email_uniqueness(email=user_in.email, current_user_id=current_user.id, db=db)
    return UserService.update_user_full(db=db, user_id=current_user.id, user_data=user_in)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de usuario (PATCH)",
    description="Modifica uno o múltiples campos específicos de un usuario en la base de datos. Lanza un error 400 si el cuerpo del JSON está vacío."
)
def update_user_partial(
    user_in: UserPatch,
    current_user: User = Depends(get_valid_user_or_404),
    db: Session = Depends(get_db)
):
    payload_data = user_in.model_dump(exclude_unset=True)
    if not payload_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar"
        )
    
    if "email" in payload_data:
        verify_email_uniqueness(email=payload_data["email"], current_user_id=current_user.id, db=db)
        
    return UserService.update_user_partial(db=db, user_id=current_user.id, user_data=user_in)
