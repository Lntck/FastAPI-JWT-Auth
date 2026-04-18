from app.crud import UserCRUD
from app.core import myctx
from app.exceptions import UserNotFound, UserAlreadyExists
from app.schemas import UserRead, UserCreate, UserInDB

from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, user_crud: UserCRUD):
        self.user_crud = user_crud
    
    async def create_user(self, session: AsyncSession, user: UserCreate) -> UserRead:
        if await self.user_crud.get_by_username(session, user.username):
            raise UserAlreadyExists()

        hashed_psw = myctx.hash(user.password.get_secret_value())

        user_in_db = UserInDB(
            username=user.username,
            email=user.email,
            password_hash=hashed_psw,
        )

        db_user = await self.user_crud.create_user(session, user_in_db)

        return UserRead.model_validate(db_user)

    async def get_by_username(self, session: AsyncSession, username: str) -> UserRead:
        user = await self.user_crud.get_by_username(session, username)
        if not user:
            raise UserNotFound()
        return UserRead.model_validate(user)

    async def get_by_username_with_password(self, session: AsyncSession, username: str) -> UserInDB:
        user = await self.user_crud.get_by_username(session, username)
        if not user:
            raise UserNotFound()
        return UserInDB.model_validate(user)
    
    async def get_all_users(self, session: AsyncSession) -> list[UserRead]:
        users = await self.user_crud.get_all_users(session)
        return [
            UserRead.model_validate(user)
            for user in users
        ]
