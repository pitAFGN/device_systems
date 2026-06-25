from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService
from app.auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Crear un préstamo")
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
        
    return LoanService.create(db, loan_data)

@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Registrar devolución de dispositivo")
def return_device(loan_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
    
    # Permitir Admin o Support
    if payload.get("role") not in ["admin", "support"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos suficientes para procesar devoluciones.")
        
    return LoanService.process_return(db, loan_id)

@router.get("/details", response_model=List[LoanDetailResponse], summary="Ver detalles de todos los préstamos")
def get_loan_details(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
    
    # Permitir Admin o Support
    if payload.get("role") not in ["admin", "support"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado a reportes detallados.")
        
    return LoanService.get_all_details(db)