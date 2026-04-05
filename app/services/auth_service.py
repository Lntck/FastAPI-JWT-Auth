from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.security import myctx, JWTManager
from app.core.exceptions import UserAlreadyExists, TokenInvalidError
from app.crud.user import UserCRUD 
from app.schemas.user import UserInDB, UserCreate, UserRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService:
    def __init__(self, user_crud: UserCRUD):
        self.user_crud = user_crud
        self.jwt_manager = JWTManager()
    
    def register_user(self, user: UserCreate) -> UserRead:
        if self.user_crud.get_by_username(user.username):
            raise UserAlreadyExists("User with this username already exists")

        hashed_psw = myctx.hash(user.password)
        return self.user_crud.register(UserInDB(username=user.username, hashed_password=hashed_psw))
    
    def auth_user(self, username: str, password: str) -> tuple[UserInDB | None, str | None]:
        user = self.user_crud.get_by_username(username)
        if user is None:
            return None, None
        if not myctx.verify(password, user.hashed_password):
            return None, None

        token = self.jwt_manager.create_token({"sub": user.username}, settings.access_secret, settings.access_token_expire_m)
        return user, token

    def get_user_from_token(self, token: str) -> str:
        payload = self.jwt_manager.decode_token(token, settings.access_secret)

        if not payload or "sub" not in payload:
            raise TokenInvalidError("Invalid token payload")

        return payload["sub"]
