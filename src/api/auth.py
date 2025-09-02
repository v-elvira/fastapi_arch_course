from datetime import datetime, timedelta, timezone
import jwt  # PyJWT in requirements

from fastapi import APIRouter, Response, status, HTTPException
from passlib.context import CryptContext

from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.repositories.users import UsersRepository

router = APIRouter(prefix='/auth', tags=['User auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login')
async def login_user(user_data: UserRequestAdd) -> dict:
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Wrong email/password')
        access_token = create_access_token({'user_id': user.id})
        return {'access_token': access_token}

@router.post('/register')
async def register(user_data: UserRequestAdd, response: Response) -> dict[str, str | User]:
    new_data = UserRequestAdd.model_dump(user_data)
    new_data['hashed_password'] = pwd_context.hash(user_data.password)
    del new_data['password']
    new_user_data = UserAdd(**new_data)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        if not user:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': f'Failed: user with email {user_data.email} already exists'}
        await session.commit()
    return {'status': 'OK', 'user': user}
