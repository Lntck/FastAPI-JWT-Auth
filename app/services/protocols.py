from typing import Any, Protocol

from app.models import User


class UserServiceProtocol(Protocol):
    async def get_by_id(self, session: Any, user_id: int) -> User:
        ...

    async def get_by_username(self, session: Any, username: str) -> User:
        ...
