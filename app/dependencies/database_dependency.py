from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user_model import User

# Dependencia obligatoria de la Fase 7: Entrega una sesión de base de datos
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia auxiliar: Busca un usuario por ID en la BD o lanza 404
def get_valid_user_or_404(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado."
        )
    return db_user

# Dependencia auxiliar: Verifica la unicidad del email en la BD o lanza 400
def verify_email_uniqueness(email: str, current_user_id: Optional[int] = None, db: Session = Depends(get_db)) -> None:
    query = db.query(User).filter(User.email == email)
    
    # Si estamos actualizando, excluimos el ID del usuario actual de la verificación
    if current_user_id is not None:
        query = query.filter(User.id != current_user_id)
        
    existing_user = query.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ingresado ya se encuentra registrado."
        )