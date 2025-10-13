from datetime import datetime, timedelta, timezone
import jwt  # PyJWT in requirements
from fastapi import HTTPException

from passlib.context import CryptContext
from src.config import settings
from src.services.base import BaseService

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {'exp': expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail='Invalid token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired token')
