from fastapi import HTTPException, status, Path
from app.services.user_service import UserService

def get_valid_user_or_404(user_id: int = Path(..., description="ID numérico del usuario a buscar", gt=0)) -> dict:
    """Busca un usuario por su ID. Si no existe, lanza un error 404."""
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

def verify_email_uniqueness(email: str, current_user_id: int = None):
    """Verifica que el email no esté registrado por otro usuario."""
    existing_user = UserService.get_user_by_email(email)
    if existing_user and existing_user["id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado"
        )