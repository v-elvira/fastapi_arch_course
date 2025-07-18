from fastapi import APIRouter, Response, status
from passlib.context import CryptContext
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.repositories.users import UsersRepository

router = APIRouter(prefix='/auth', tags=['User auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
