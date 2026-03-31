import jwt
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

from app.core.exceptions import TokenExpiredError, TokenInvalidError


myctx = CryptContext(schemes=["argon2"], deprecated="auto")


class JWTManager:
    @staticmethod
    def create_token(payload: dict, secret_key: str, expires_minutes: int) -> str:
        data_to_encode = payload.copy()

        data_to_encode.update(
            {
                "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
                "iat": datetime.now(timezone.utc)
            }
        )

        return jwt.encode(data_to_encode, secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token: str, secret_key: str) -> dict | None:
        try:
            return jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token is expired")
        except jwt.InvalidTokenError as e:
            raise TokenInvalidError(f"Invalid token: {e}")
