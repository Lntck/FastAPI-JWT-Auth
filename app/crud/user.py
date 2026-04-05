from app.schemas.user import UserInDB, UserRead


DataBase = {}


class UserCRUD:
    def __init__(self):
        self.db = DataBase
    
    def register(self, user: UserInDB) -> UserRead:
        self.db[user.username] = user
        return UserRead(username=user.username)

    def get_by_username(self, username: str) -> UserInDB | None:
        return self.db.get(username)