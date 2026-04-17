from fastapi import Depends

from app.api.dependencies.repositories import get_user_crud
from app.core.config import Settings, get_settings
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.crud.user import UserCRUD


def get_auth_service(user_crud: UserCRUD = Depends(get_user_crud), settings: Settings = Depends(get_settings)):
    return AuthService(user_crud, settings)

def get_user_service(user_crud: UserCRUD = Depends(get_user_crud)):
    return UserService(user_crud)