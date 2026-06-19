from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/", response_model=List[DeviceResponse], summary="Listar dispositivos", description="Obtiene todos los dispositivos registrados. Permite filtrar por tipo, marca, disponibilidad o realizar búsquedas generales.")
def get_devices(
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return DeviceService.get_all(db, device_type, is_available, brand, search)

@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo por ID")
def get_device(device_id: int, db: Session = Depends(get_db)):
    return DeviceService.get_by_id(db, device_id)

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo dispositivo")
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    return DeviceService.create(db, device_data)

@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo (Completo)")
def update_device_full(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService.update(db, device_id, device_data)

@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo (Parcial)")
def update_device_partial(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService.update(db, device_id, device_data)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un dispositivo")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    DeviceService.delete(db, device_id)
    return None