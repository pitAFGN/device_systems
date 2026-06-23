import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user", description="Roles: admin, support, user")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no debe contener espacios en blanco.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir al menos un número.")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        allowed_roles = ["admin", "support", "user"]
        if value not in allowed_roles:
            raise ValueError(f"Rol no permitido. Debe ser uno de: {', '.join(allowed_roles)}")
        return value

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None