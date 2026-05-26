from pydantic import BaseModel, Field, EmailStr
from typing import Literal

# Modelo base con los atributos comunes
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Correo electrónico con formato válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Rol asignado en el sistema")
    is_active: bool = Field(default=True, description="Estado de actividad del usuario")

# Modelo para la creación (Entrada)
class UserCreate(UserBase):
    pass

# Modelo para la respuesta (Salida)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True