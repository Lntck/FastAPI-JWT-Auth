from sqlalchemy.ext.asyncio import AsyncSession

from app.core import JWTManager, Settings, myctx
from app.exceptions import InvalidCredentials, TokenInvalidError
from app.services.user_service import UserService


RefreshTokens = {}


class AuthService:
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    def __init__(self, user_service: UserService, settings: Settings):
        self.user_service = user_service
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

    async def auth_user(self, session: AsyncSession, username: str, password: str) -> tuple[str, str]:
        user = await self.user_service.get_by_username_with_password(session, username)

        if not user or not myctx.verify(password, user.password_hash):
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
        
        RefreshTokens.setdefault(user.username, set()).add(refresh_token)
        
        return access_token, refresh_token

    async def refresh_token(self, session: AsyncSession, refresh_token: str) -> tuple[str, str]:
        payload = self.jwt_manager.decode_token(refresh_token, self.settings.refresh_secret)
        username = self._validate_token_payload(payload, self.REFRESH_TOKEN_TYPE, "Invalid refresh token")
        user = await self.user_service.get_by_username(session, username)

        if not user:
            raise TokenInvalidError("User not found")
        
        if refresh_token not in RefreshTokens.get(username, ()):
            raise TokenInvalidError("Refresh token is invalid")
        RefreshTokens[username].remove(refresh_token)

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

        RefreshTokens.setdefault(user.username, set()).add(new_refresh_token)

        return new_access_token, new_refresh_token
    
    async def remove_refresh_token(self, session: AsyncSession, refresh_token: str) -> None:
        payload = self.jwt_manager.decode_token(refresh_token, self.settings.refresh_secret)
        username = self._validate_token_payload(payload, self.REFRESH_TOKEN_TYPE, "Invalid refresh token")
        user = await self.user_service.get_by_username(session, username)

        if not user:
            raise TokenInvalidError("User not found")

        if refresh_token not in RefreshTokens.get(username, ()):
            raise TokenInvalidError("Refresh token is invalid")
        RefreshTokens[username].remove(refresh_token)

    def get_user_from_token(self, token: str) -> str:
        payload = self.jwt_manager.decode_token(token, self.settings.access_secret)
        return self._validate_token_payload(payload, self.ACCESS_TOKEN_TYPE, "Invalid access token")
