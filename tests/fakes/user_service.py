from app.models import User
from app.core import myctx


class FakeUserService:
    async def get_by_id(self, session, user_id):
        return User(id=user_id, username="tester", email="tester@example.com", password_hash=myctx.hash("password"))

    async def get_by_username(self, session, username):
        return User(id=1, username=username, email=f"{username}@example.com", password_hash=myctx.hash("password"))