from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Esquema base con campos comunes
class DeviceBase(BaseModel):
    name: str = Field(..., examples=["Laptop Lenovo ThinkPad"])
    serial_number: str = Field(..., examples=["LEN-2024-001"])
    device_type: str = Field(..., examples=["laptop"]) # laptop, tablet, proyector, etc.
    brand: Optional[str] = Field(None, examples=["Lenovo"])

# Esquema para crear un dispositivo (POST)
class DeviceCreate(DeviceBase):
    pass

# Esquema para actualizar un dispositivo (PUT/PATCH)
class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Laptop Lenovo ThinkPad Ev1"])
    serial_number: Optional[str] = Field(None, examples=["LEN-2024-001"])
    device_type: Optional[str] = Field(None, examples=["laptop"])
    brand: Optional[str] = Field(None, examples=["Lenovo"])
    is_available: Optional[bool] = Field(None, examples=[True])

# Esquema para las respuestas de la API
class DeviceResponse(DeviceBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True