from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr
from datetime import datetime


# Base User schema with common fields
class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=24)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

# Schema for creating a new user, includes password
class UserCreate(UserBase):
    password: SecretStr = Field(..., min_length=8, max_length=24)

# Schema for reading user data, excludes password
class UserRead(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime

# Schema for user data stored in the database, includes hashed password
class UserInDB(UserBase):
    password_hash: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"