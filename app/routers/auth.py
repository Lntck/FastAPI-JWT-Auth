from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import TokenExpiredError, TokenInvalidError, UserAlreadyExists
from app.schemas.user import Token, UserCreate, UserRead
from app.services.auth_service import AuthService, oauth2_scheme
from app.crud.user import UserCRUD


router = APIRouter()


def get_user_crud():
    return UserCRUD()


def get_auth_service(user_crud: UserCRUD = Depends(get_user_crud)):
    return AuthService(user_crud)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> str:
    try:
        return service.get_user_from_token(token)
    except TokenExpiredError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except TokenInvalidError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register_user(user)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    user, token = service.auth_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/about_me", response_model=UserRead)
async def about(
    current_user: str = Depends(get_current_user),
    user_crud: UserCRUD = Depends(get_user_crud),
):
    user = user_crud.get_by_username(current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_id = user_crud.db.index(user) + 1 if user in user_crud.db else 0
    return UserRead(id=user_id, username=user.username)
