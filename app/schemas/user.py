from pydantic import BaseModel, Field


class UserInDB(BaseModel):
    username: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=4, max_length=24)
    password: str = Field(..., min_length=8, max_length=24)

class UserRead(BaseModel):
    id: int
    username: str