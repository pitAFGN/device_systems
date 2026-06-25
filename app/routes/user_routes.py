from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.database_dependency import get_db
# Asegúrate de importar tus esquemas y servicios correspondientes
# de acuerdo a cómo los tengas nombrados en tu proyecto
from app.schemas.user_schema import UserResponse 
from app.services.user_service import UserService
from app.auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse], summary="Listar usuarios")
def get_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
    
    return UserService.get_all(db)

@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
        
    return UserService.get_by_id(db, user_id)