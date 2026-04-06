from app.schemas.user import UserInDB, UserRead


DataBase = {}
RefreshTokens = {}


class UserCRUD:
    def __init__(self):
        self.db = DataBase
        self.refresh_tokens = RefreshTokens
    
    def register(self, user: UserInDB) -> UserRead:
        self.db[user.username] = user
        return UserRead(username=user.username)

    def get_by_username(self, username: str) -> UserInDB | None:
        return self.db.get(username)