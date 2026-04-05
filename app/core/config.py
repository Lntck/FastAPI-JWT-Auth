from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "DATABASE_URL"
    access_secret: str = "SECRET_KEY_ACCESS"
    refresh_secret: str = "SECRET_KEY_REFRESH"
    access_token_expire_m: int = 1440           # 1 day
    refresh_token_expire_m: int = 10080         # 7 days

    class Config:
        env_file = ".env"
        frozen = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
