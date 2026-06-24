from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database.connection import get_db 
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserResponse, Token
from app.auth.auth_service import AuthService # <── Importamos el servicio
from app.dependencies.auth_dependency import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, user_in: UserRegister, db: Session = Depends(get_db)):

    return AuthService.register_user(db=db, user_in=user_in)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Delegamos la autenticación y generación de token al servicio
    return AuthService.authenticate_user(db=db, form_data=form_data)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user