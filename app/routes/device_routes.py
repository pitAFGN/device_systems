from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer  # ──> Importamos esto aquí localmente
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services.device_service import DeviceService

# Importamos la función de decodificación que tienes en tu security.py
from app.auth.security import decode_access_token 

# Le decimos a Swagger que busque el token en el endpoint de login de tu AuthRouter
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/devices", tags=["Devices"])

# ──> TUS MÉTODOS GET SE QUEDAN EXACTAMENTE IGUAL...
@router.get("/", response_model=List[DeviceResponse], summary="Listar dispositivos")
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
def create_device(
    device_data: DeviceCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) 
):

    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        )
    
    user_role = payload.get("role")
    
    
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos suficientes para realizar esta acción."
        )
        
    return DeviceService.create(db, device_data)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo (Completo)")
def update_device_full(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService.update(db, device_id, device_data)

@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo (Parcial)")
def update_device_partial(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService.update(db, device_id, device_data)