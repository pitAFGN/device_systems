from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# Valores permitidos para el rol: admin, support, user.
AllowedRoles = Literal["admin", "support", "user"]

class UserBase(BaseModel):
    # name: obligatorio, mínimo 3 caracteres.
    name: str = Field(..., min_length=3, max_length=50, examples=["Juan Pérez"])
    # email: formato válido.
    email: EmailStr = Field(..., examples=["juan.perez@example.com"])
    # role: valores permitidos: admin, support, user.
    role: AllowedRoles = Field(..., examples=["user"])
    # is_active: booleano.
    is_active: bool = Field(default=True)

# Schema para: Crear usuario
class UserCreate(UserBase):
    pass

# Schema para: Actualizar usuario completo (UserUpdate)
class UserUpdate(UserBase):
    """
    Reutiliza UserBase porque obliga al cliente a enviar TODOS 
    los campos obligatorios para reemplazar el recurso por completo (PUT).
    """
    pass

# Schema para: Actualizar usuario parcial (UserPatch)
class UserPatch(BaseModel):
    """
    Todos los campos se vuelven opcionales (Optional) para permitir
    modificar solo los atributos que el cliente envíe (PATCH).
    """
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None)
    role: Optional[AllowedRoles] = Field(None)
    is_active: Optional[bool] = Field(None)

# Schema para: Responder usuario
class UserResponse(UserBase):
    id: int
    created_at: datetime  # Incluido para retornar la fecha guardada en el modelo

    class Config:
        # Permite mapear los objetos ORM de SQLAlchemy directamente a JSON
        from_attributes = True