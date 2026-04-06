from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_auth_service
from app.schemas.user import Token, UserCreate, UserRead
from app.services.auth_service import AuthService
from app.core.rate_limit import limiter


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register(request: Request, user: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register_user(user)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    access_token, refresh_token = service.auth_user(form_data.username, form_data.password)

    print(f"Generated access token: {access_token}")
    print(f"Generated refresh token: {refresh_token}")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True,
                        secure=True, samesite="strict", max_age=60 * service.settings.refresh_token_expire_m)

    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token)
@limiter.limit("3/minute")
async def refresh(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token", "")

    access_token, new_refresh_token = service.refresh_token(refresh_token)

    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True,
                        secure=True, samesite="strict", max_age=60 * service.settings.refresh_token_expire_m)

    return Token(access_token=access_token)
