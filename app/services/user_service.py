from app.data.users_db import users_database
from app.schemas.user_schema import UserCreate, UserUpdateFull, UserUpdatePartial
from typing import List, Optional

class UserService:
    @staticmethod
    def get_all_users(role: Optional[str] = None, is_active: Optional[bool] = None) -> List[dict]:
        filtered_users = users_database
        if role:
            filtered_users = [u for u in filtered_users if u["role"] == role]
        if is_active is not None:
            filtered_users = [u for u in filtered_users if u["is_active"] == is_active]
        return filtered_users

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        for user in users_database:
            if user["id"] == user_id:
                return user
        return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        for user in users_database:
            if user["email"].lower() == email.lower():
                return user
        return None

    @staticmethod
    def create_user(user_data: UserCreate) -> dict:
        new_id = max([u["id"] for u in users_database], default=0) + 1
        new_user = user_data.model_dump()
        new_user["id"] = new_id
        users_database.append(new_user)
        return new_user

    @staticmethod
    def update_user_full(user_id: int, user_data: UserUpdateFull) -> dict:
        for user in users_database:
            if user["id"] == user_id:
                user.update(user_data.model_dump())
                return user
        return {}

    @staticmethod
    def update_user_partial(user_id: int, user_data: UserUpdatePartial) -> dict:
        for user in users_database:
            if user["id"] == user_id:
                # Filtrar campos no enviados (None) de forma explícita
                update_dict = user_data.model_dump(exclude_unset=True)
                user.update(update_dict)
                return user
        return {}

    @staticmethod
    def delete_user(user_id: int) -> bool:
        for index, user in enumerate(users_database):
            if user["id"] == user_id:
                users_database.pop(index)
                return True
        return False