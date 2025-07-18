from pydantic import EmailStr
from src.schemas.common import CommonBaseModel

class UserRequestAdd(CommonBaseModel):
    email: EmailStr
    password: str

class UserAdd(CommonBaseModel):
    email: EmailStr
    hashed_password: str

class User(CommonBaseModel):
    id: int
    email: EmailStr
