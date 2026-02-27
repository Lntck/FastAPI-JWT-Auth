from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "DATABASE_URL"
    secret_key: str = "SECRET_KEY"
    debug: bool = False

    class Config:
        env_file = ".env"
        frozen = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = Settings()