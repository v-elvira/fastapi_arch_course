from pydantic import EmailStr, Field
from src.schemas.common import CommonBaseModel


class UserRequestAdd(CommonBaseModel):
    email: EmailStr
    password: str = Field(min_length=2, max_length=100)


class UserAdd(CommonBaseModel):
    email: EmailStr
    hashed_password: str


class User(CommonBaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_password: str
