from datetime import datetime, timedelta, timezone
import jwt  # PyJWT in requirements

from passlib.context import CryptContext
from src.config import settings
from src.exceptions import WrongEmailPasswordException, InvalidTokenException, ExpiredTokenException, \
    ObjectExistsException, UserExistsException
from src.schemas.users import UserRequestAdd, UserAdd
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
            raise InvalidTokenException
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException

    async def login_user(self, user_data: UserRequestAdd) -> str:
            user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
            if not user or not self.verify_password(user_data.password, user.hashed_password):
                raise WrongEmailPasswordException
            return self.create_access_token({'user_id': user.id})

    async def register(self, user_data: UserRequestAdd):
            new_data = UserRequestAdd.model_dump(user_data)
            new_data['hashed_password'] = self.hash_password(user_data.password)
            del new_data['password']
            new_user_data = UserAdd(**new_data)
            try:
                user = await self.db.users.add(new_user_data)
            except ObjectExistsException:
                raise UserExistsException
            await self.db.commit()
            return user

    async def get_user(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user
