from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.dependencies.services import get_auth_service
from app.services.auth_service import AuthService
from app.core.constants import API_V1_PREFIX


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_PREFIX}/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> str:
    return service.get_user_from_token(token)