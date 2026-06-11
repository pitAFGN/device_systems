from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """• Crear usuario."""
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            is_active=user_data.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_all_users(
        db: Session, 
        role: Optional[str] = None, 
        is_active: Optional[bool] = None,
        sort_by: Optional[str] = "name"
    ) -> List[User]:
        """
        • Listar usuarios.
        • Filtrar usuarios por rol.
        • Filtrar usuarios por estado.
        • Ordenar usuarios por nombre o fecha de creación.
        """
        query = db.query(User)
        
        # Filtrado por rol
        if role:
            query = query.filter(User.role == role)
            
        # Filtrado por estado (is_active)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
            
        # Ordenamiento por nombre o fecha de creación
        if sort_by == "created_at":
            query = query.order_by(User.created_at.desc())
        else:
            query = query.order_by(User.name.asc())
            
        return query.all()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """• Buscar usuario por ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """• Buscar usuario por email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_user_full(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """• Actualizar usuario completo."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.name = user_data.name
            db_user.email = user_data.email
            db_user.role = user_data.role
            db_user.is_active = user_data.is_active
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user_partial(db: Session, user_id: int, user_data: UserPatch) -> Optional[User]:
        """• Actualizar usuario parcial."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Convierte el esquema a diccionario ignorando los campos no enviados por el cliente
            payload_data = user_data.model_dump(exclude_unset=True)
            for key, value in payload_data.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """• Eliminar usuario."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    