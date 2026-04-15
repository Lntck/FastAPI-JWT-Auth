from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "DATABASE_URL"
    access_secret: str = "CHANGE_ME_ACCESS_SECRET_MIN_32_CHARS"
    refresh_secret: str = "CHANGE_ME_REFRESH_SECRET_MIN_32_CHARS"
    access_token_expire_m: int = 15  # 15 minutes
    refresh_token_expire_m: int = 43200  # 30 days
    cookie_secure: bool = True
    cookie_samesite: Literal["lax", "strict", "none"] = "strict"

    @field_validator("access_secret", "refresh_secret")
    @classmethod
    def validate_secret_length(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT secret must be at least 32 characters long")
        return value

    class Config:
        env_file = ".env"
        frozen = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
