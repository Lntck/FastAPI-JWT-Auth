from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_user_service
from app.schemas import UserRead
from app.services import UserService
from app.db import db_helper


router = APIRouter()


@router.get("/about_me", response_model=UserRead)
async def about(
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
    service: UserService = Depends(get_user_service),
):
    return await service.get_by_username(session=session, username=current_user)
