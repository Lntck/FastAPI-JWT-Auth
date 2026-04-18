from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserInDB
from app.models import User


class UserCRUD:
    def __init__(self):
        pass

    async def create_user(self, session: AsyncSession, user_in_db: UserInDB) -> User:
        user = User(**user_in_db.model_dump())
        session.add(user)
        await session.commit()
        return user

    async def get_by_username(self, session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.scalar(stmt)
        return result

    async def get_all_users(self, session: AsyncSession) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()