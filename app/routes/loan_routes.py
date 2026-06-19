from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.get("/", response_model=List[LoanDetailResponse], summary="Listar préstamos detallados", description="Devuelve los registros históricos de préstamos incluyendo los datos completos del usuario y del dispositivo asociado (Joins).")
def get_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return LoanService.get_all_loans(db, status, user_email, device_type)

@router.get("/{loan_id}", response_model=LoanDetailResponse, summary="Obtener préstamo detallado por ID")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return LoanService.get_by_id(db, loan_id)

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un préstamo", description="Crea un préstamo vinculando un usuario y un dispositivo. Cambia el estado del dispositivo automáticamente a no disponible.")
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    return LoanService.create_loan(db, loan_data)

@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver un dispositivo", description="Registra la devolución de un equipo tecnológico, marcando el préstamo como 'returned' y volviendo a habilitar el dispositivo.")
def return_device(loan_id: int, db: Session = Depends(get_db)):
    return LoanService.return_loan(db, loan_id)

# Endpoints adicionales solicitados en la Fase 10 para búsquedas por entidad específica:
@router.get("/user/{user_id}", response_model=List[LoanDetailResponse], summary="Consultar préstamos de un usuario", tags=["Users"])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    return LoanService.get_loans_by_user(db, user_id)

@router.get("/device/{device_id}", response_model=List[LoanDetailResponse], summary="Consultar historial de préstamos de un dispositivo")
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return LoanService.get_loans_by_device(db, device_id)