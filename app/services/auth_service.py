from fastapi.security import HTTPBasicCredentials

from app.core.security import myctx
from app.crud.user import UserCRUD 
from app.schemas.user import UserInDB, UserCreate, UserRead


class AuthService:
    def __init__(self, user_crud: UserCRUD):
        self.user_crud = user_crud
    
    def register_user(self, user: UserCreate) -> UserRead:
        if self.user_crud.get_by_username(user.username):
            raise ValueError("User with this username already exists")
        hashed_psw = myctx.hash(user.password)
        return self.user_crud.register(UserInDB(username=user.username, hashed_password=hashed_psw))
    
    def auth_user(self, credentials: HTTPBasicCredentials) -> UserInDB | None:
        user = self.user_crud.get_by_username(credentials.username)
        if user is None: return None
        if not myctx.verify(credentials.password, user.hashed_password): return None
        return user
