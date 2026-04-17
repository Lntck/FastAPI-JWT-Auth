from app.crud.user import UserCRUD
from app.exceptions.custom import UserNotFound
from app.schemas.user import UserRead


class UserService:
    def __init__(self, user_crud: UserCRUD):
        self.user_crud = user_crud

    def get_profile(self, username: str) -> UserRead:
        user = self.user_crud.get_by_username(username)
        if not user:
            raise UserNotFound()
        return UserRead(username=user.username)
