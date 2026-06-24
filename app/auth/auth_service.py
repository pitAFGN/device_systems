from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token

class AuthService:
    
    @staticmethod
    def register_user(db: Session, user_in: UserRegister) -> User:
        db_user = db.query(User).filter(User.email == user_in.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El correo electrónico ya se encuentra registrado."
            )
        
        hashed_pass = get_password_hash(user_in.password)
        
        # Mapeo corregido apuntando a la columna real del modelo
        new_user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=hashed_pass,  # <── Validado con tu user_model.py
            role=user_in.role,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
        user = db.query(User).filter(User.email == form_data.username).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password): 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de acceso incorrectas.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}