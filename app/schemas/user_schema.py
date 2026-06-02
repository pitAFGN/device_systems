from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# 1. Esto es nuevo: Restringir los roles válidos a nivel de código
AllowedRoles = Literal["admin", "user", "support"]

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, examples=["Juan Pérez"])
    email: EmailStr = Field(..., examples=["juan.perez@example.com"])
    role: AllowedRoles = Field(..., examples=["user"]) # Usa el validador de roles
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    pass

# ==========================================
# NUEVOS ESQUEMAS PARA ESTA ACTIVIDAD
# ==========================================

class UserUpdateFull(UserBase):
    """
    Para el PUT: Reutiliza UserBase porque obliga al cliente 
    a enviar TODOS los campos para reemplazar el usuario.
    """
    pass

class UserUpdatePartial(BaseModel):
    """
    Para el PATCH: OBLIGATORIO que todos los campos sean opcionales (Optional).
    Si el cliente solo manda el 'role', Pydantic ignorará el resto sin fallar.
    """
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None)
    role: Optional[AllowedRoles] = Field(None)
    is_active: Optional[bool] = Field(None)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True