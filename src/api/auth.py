from fastapi import APIRouter, Response, status, HTTPException

from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.repositories.users import UsersRepository
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['User auth'])

@router.post('/login')
async def login_user(user_data: UserRequestAdd, response: Response) -> dict:
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user or not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Wrong email/password')
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}

@router.post('/register')
async def register(user_data: UserRequestAdd, response: Response) -> dict[str, str | User]:
    new_data = UserRequestAdd.model_dump(user_data)
    new_data['hashed_password'] = AuthService().hash_password(user_data.password)
    del new_data['password']
    new_user_data = UserAdd(**new_data)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        if not user:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': f'Failed: user with email {user_data.email} already exists'}
        await session.commit()
    return {'status': 'OK', 'user': user}
