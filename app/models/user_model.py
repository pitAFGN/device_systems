from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    # id: Integer, Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # name: String, Obligatorio
    name = Column(String, nullable=False)
    
    # email: String, Único y obligatorio
    email = Column(String, unique=True, nullable=False, index=True)
    
    # role: String, Obligatorio
    role = Column(String, nullable=False)
    
    # is_active: Boolean, Valor por defecto True
    is_active = Column(Boolean, default=True)
    
    # created_at: DateTime, Fecha de creación
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))