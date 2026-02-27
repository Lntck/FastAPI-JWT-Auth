from app.schemas.user import UserInDB, UserCreate, UserRead

import hmac


class UserCRUD:
    def __init__(self):
        self.db = []
    
    def register(self, user: UserInDB) -> UserRead:
        self.db.append(user)
        return UserRead(id=len(self.db), username=user.username)

    def get_by_username(self, username: str) -> UserInDB | None:
        for user in self.db:
            if hmac.compare_digest(user.username, username):
                return user
        return None