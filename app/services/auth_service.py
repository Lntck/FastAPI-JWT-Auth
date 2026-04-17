from app.core.config import Settings
from app.core.security import myctx, JWTManager
from app.exceptions.custom import InvalidCredentials, UserAlreadyExists, TokenInvalidError
from app.crud.user import UserCRUD 
from app.schemas.user import UserInDB, UserCreate, UserRead


class AuthService:
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    def __init__(self, user_crud: UserCRUD, settings: Settings):
        self.user_crud = user_crud
        self.settings = settings
        self.jwt_manager = JWTManager()

    @staticmethod
    def _validate_token_payload(payload: dict | None, expected_type: str, invalid_message: str) -> str:
        if not payload:
            raise TokenInvalidError(invalid_message)

        username = payload.get("sub")
        token_type = payload.get("type")
        token_jti = payload.get("jti")

        if not isinstance(username, str) or not username:
            raise TokenInvalidError(invalid_message)

        if token_type != expected_type:
            raise TokenInvalidError(invalid_message)

        if not isinstance(token_jti, str) or not token_jti:
            raise TokenInvalidError(invalid_message)

        return username

    def register_user(self, user: UserCreate) -> UserRead:
        if self.user_crud.get_by_username(user.username):
            raise UserAlreadyExists()

        hashed_psw = myctx.hash(user.password)
        return self.user_crud.register(UserInDB(username=user.username, hashed_password=hashed_psw))
    
    def auth_user(self, username: str, password: str) -> tuple[str, str]:
        user = self.user_crud.get_by_username(username)

        if not user or not myctx.verify(password, user.hashed_password):
            raise InvalidCredentials()

        access_token = self.jwt_manager.create_token(
            {"sub": user.username, "type": self.ACCESS_TOKEN_TYPE},
            self.settings.access_secret,
            self.settings.access_token_expire_m,
        )
        refresh_token = self.jwt_manager.create_token(
            {"sub": user.username, "type": self.REFRESH_TOKEN_TYPE},
            self.settings.refresh_secret,
            self.settings.refresh_token_expire_m,
        )
        
        self.user_crud.refresh_tokens.setdefault(user.username, set()).add(refresh_token)
        
        return access_token, refresh_token

    def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        payload = self.jwt_manager.decode_token(refresh_token, self.settings.refresh_secret)
        username = self._validate_token_payload(payload, self.REFRESH_TOKEN_TYPE, "Invalid refresh token")
        user = self.user_crud.get_by_username(username)

        if not user:
            raise TokenInvalidError("User not found")
        
        if refresh_token not in self.user_crud.refresh_tokens.get(username, ()):
            raise TokenInvalidError("Refresh token is invalid")
        self.user_crud.refresh_tokens[username].remove(refresh_token)

        new_access_token = self.jwt_manager.create_token(
            {"sub": user.username, "type": self.ACCESS_TOKEN_TYPE},
            self.settings.access_secret,
            self.settings.access_token_expire_m,
        )
        new_refresh_token = self.jwt_manager.create_token(
            {"sub": user.username, "type": self.REFRESH_TOKEN_TYPE},
            self.settings.refresh_secret,
            self.settings.refresh_token_expire_m,
        )

        self.user_crud.refresh_tokens.setdefault(user.username, set()).add(new_refresh_token)

        return new_access_token, new_refresh_token
    
    def remove_refresh_token(self, refresh_token: str) -> None:

        payload = self.jwt_manager.decode_token(refresh_token, self.settings.refresh_secret)
        username = self._validate_token_payload(payload, self.REFRESH_TOKEN_TYPE, "Invalid refresh token")
        user = self.user_crud.get_by_username(username)

        if not user:
            raise TokenInvalidError("User not found")

        if refresh_token not in self.user_crud.refresh_tokens.get(username, ()):
            raise TokenInvalidError("Refresh token is invalid")
        self.user_crud.refresh_tokens[username].remove(refresh_token)

    def get_user_from_token(self, token: str) -> str:
        payload = self.jwt_manager.decode_token(token, self.settings.access_secret)
        return self._validate_token_payload(payload, self.ACCESS_TOKEN_TYPE, "Invalid access token")
