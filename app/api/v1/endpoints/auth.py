from contextlib import suppress

from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.services import get_auth_service
from app.exceptions.custom import TokenExpiredError, TokenInvalidError
from app.schemas.user import Token, UserCreate, UserRead
from app.services.auth_service import AuthService
from app.api.middlewares.rate_limit import limiter
from app.utils.http import set_refresh_cookie


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register(request: Request, user: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register_user(user)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    access_token, refresh_token = service.auth_user(form_data.username, form_data.password)

    set_refresh_cookie(response, refresh_token, service)

    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token)
@limiter.limit("3/minute")
async def refresh(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token", "")

    access_token, new_refresh_token = service.refresh_token(refresh_token)

    set_refresh_cookie(response, new_refresh_token, service)

    return Token(access_token=access_token)


@router.post("/logout")
@limiter.limit("3/minute")
async def logout(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token", "")

    if refresh_token:
        with suppress(TokenInvalidError, TokenExpiredError):
            service.remove_refresh_token(refresh_token)

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=service.settings.cookie_secure,
        samesite=service.settings.cookie_samesite,
        path="/",
    )

    return {"message": "logout successfully!"}