from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_user_service
from app.services.user_service import UserService
from app.schemas.user import UserRead


router = APIRouter()


@router.get("/about_me", response_model=UserRead)
async def about(
    current_user: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.get_profile(username=current_user)
