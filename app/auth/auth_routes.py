from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database.connection import get_db  # Verifica que esta sea tu ruta exacta a get_db
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserResponse, Token
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.dependencies.auth_dependency import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, user_in: UserRegister, db: Session = Depends(get_db)):
    # 1. Validar que el email sea único
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya se encuentra registrado."
        )
    
    # 2. Aplicar Hash a la contraseña antes de guardarla
    hashed_pass = get_password_hash(user_in.password)
    
    # 3. Crear el nuevo usuario
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_pass,
        role=user_in.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar al usuario por su email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Validar usuario y verificar contraseña con hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de acceso incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso incluyendo el email (sub) y su rol
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    # Retorna directamente el usuario logueado (protegido por token)
    return current_user