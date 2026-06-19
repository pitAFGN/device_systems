from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate
from fastapi import HTTPException, status

class DeviceService:
    
    @staticmethod
    def get_all(db: Session, device_type: str = None, is_available: bool = None, brand: str = None, search: str = None):
        query = db.query(Device)
        
        # Filtros exactos de la Fase 8
        if device_type:
            query = query.filter(Device.device_type == device_type)
        if is_available is not None:
            query = query.filter(Device.is_available == is_available)
        if brand:
            query = query.filter(Device.brand == brand)
            
        # Filtro de búsqueda avanzada de la Fase 10 (Uso de or_ y ilike)
        if search:
            query = query.filter(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.serial_number.ilike(f"%{search}%"),
                    Device.brand.ilike(f"%{search}%")
                )
            )
        return query.all()

    @staticmethod
    def get_by_id(db: Session, device_id: int):
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo inexistente")
        return device

    @staticmethod
    def create(db: Session, device_data: DeviceCreate):
        # Validación de duplicados (Fase 11)
        existing = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de serie duplicado")
        
        new_device = Device(**device_data.model_dump())
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device

    @staticmethod
    def update(db: Session, device_id: int, device_data: DeviceUpdate):
        device = DeviceService.get_by_id(db, device_id)
        
        # Validar si va a cambiar el serial por uno existente
        if device_data.serial_number and device_data.serial_number != device.serial_number:
            existing = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Número de serie duplicado")
                
        for key, value in device_data.model_dump(exclude_unset=True).items():
            setattr(device, key, value)
            
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def delete(db: Session, device_id: int):
        device = DeviceService.get_by_id(db, device_id)
        db.delete(device)
        db.commit()
        return True