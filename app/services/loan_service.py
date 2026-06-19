from sqlalchemy.orm import Session
from sqlalchemy import join
from datetime import datetime
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate
from fastapi import HTTPException, status

class LoanService:

    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate):
        # 1. Validar que el usuario exista (Fase 9 y 11)
        user_exists = db.query(User).filter(User.id == loan_data.user_id).first()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente")

        # 2. Validar que el dispositivo exista
        device = db.query(Device).filter(Device.id == loan_data.device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo inexistente")

        # 3. Validar que el dispositivo esté disponible (Fase 9 y 11) -> Genera un 409 Conflict
        if not device.is_available:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dispositivo no disponible")

        # 4. Crear el préstamo
        new_loan = Loan(
            user_id=loan_data.user_id,
            device_id=loan_data.device_id,
            status="active"
        )
        
        # 5. Cambiar disponibilidad del dispositivo a False
        device.is_available = False
        
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan

    @staticmethod
    def return_loan(db: Session, loan_id: int):
        # 1. Validar que el préstamo exista
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo inexistente")

        # 2. Validar intento de devolver un préstamo ya devuelto (Fase 11)
        if loan.status == "returned":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Intento de devolver un préstamo ya devuelto")

        # 3. Marcar como devuelto y asignar fecha actual
        loan.status = "returned"
        loan.return_date = datetime.utcnow()

        # 4. Cambiar disponibilidad del dispositivo asociado a True
        device = db.query(Device).filter(Device.id == loan.device_id).first()
        if device:
            device.is_available = True

        db.commit()
        db.refresh(loan)
        return loan

    @staticmethod
    def get_all_loans(db: Session, status_filter: str = None, user_email: str = None, device_type: str = None):
        # Usamos select_from y join para cumplir explícitamente con las consultas estructuradas de la Fase 10
        query = db.query(Loan)
        
        if status_filter:
            query = query.filter(Loan.status == status_filter)
            
        if user_email:
            query = query.join(User).filter(User.email == user_email)
            
        if device_type:
            query = query.join(Device).filter(Device.device_type == device_type)
            
        return query.all()

    @staticmethod
    def get_by_id(db: Session, loan_id: int):
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo inexistente")
        return loan

    @staticmethod
    def get_loans_by_user(db: Session, user_id: int):
        # Asegurar que el usuario existe
        user_exists = db.query(User).filter(User.id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente")
        return db.query(Loan).filter(Loan.user_id == user_id).all()

    @staticmethod
    def get_loans_by_device(db: Session, device_id: int):
        # Asegurar que el dispositivo existe
        device_exists = db.query(Device).filter(Device.id == device_id).first()
        if not device_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo inexistente")
        return db.query(Loan).filter(Loan.device_id == device_id).all()