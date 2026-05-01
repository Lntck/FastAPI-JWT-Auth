import pytest
from app.core import Settings


@pytest.fixture()
def test_settings() -> Settings:
    return Settings(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/test_db",
        redis_url="redis://localhost:6379/0",
        access_secret="a" * 32,
        refresh_secret="b" * 32,
        cookie_secure=False,
        cookie_samesite="lax",
    )