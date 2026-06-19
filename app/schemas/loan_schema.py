from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.device_schema import DeviceResponse

# Sub-esquema rápido para mostrar datos básicos del usuario dentro del préstamo
class UserMinResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

# Esquema para registrar un nuevo préstamo (POST)
class LoanCreate(BaseModel):
    user_id: int = Field(..., examples=[1])
    device_id: int = Field(..., examples=[3])

# Esquema para actualizar un préstamo (PATCH)
class LoanUpdate(BaseModel):
    status: Optional[str] = Field(None, examples=["returned"])
    return_date: Optional[datetime] = None

# Respuesta estándar de un préstamo
class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True

# FASE 7 y 10: Respuesta detallada con información relacionada (JOINS)
class LoanDetailResponse(BaseModel):
    loan_id: int = Field(..., alias="id")
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserMinResponse
    device: DeviceResponse

    class Config:
        from_attributes = True
        populate_by_name = True