from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import Settings, get_settings
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.crud.user import UserCRUD


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_crud():
    return UserCRUD()

def get_auth_service(user_crud: UserCRUD = Depends(get_user_crud), settings: Settings = Depends(get_settings)):
    return AuthService(user_crud, settings)

def get_user_service(user_crud: UserCRUD = Depends(get_user_crud)):
    return UserService(user_crud)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> str:
    return service.get_user_from_token(token)