from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService
from app.crud.user import UserCRUD


router = APIRouter()
security = HTTPBasic()


user_crud = UserCRUD()
auth_service = AuthService(user_crud)


def get_auth_service() -> AuthService:
    return auth_service


@router.post("/register")
def register(user: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), service: AuthService = Depends(get_auth_service)):
    user = service.auth_user(credentials)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": f"Welcome, {user.username}!"}