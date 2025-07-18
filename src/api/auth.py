from fastapi import APIRouter
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.repositories.users import UsersRepository

router = APIRouter(prefix='/auth', tags=['User auth'])

@router.post('/register')
async def register(user_data: UserRequestAdd) -> dict[str, str | User]:
    new_data = UserRequestAdd.model_dump(user_data)
    new_data['hashed_password'] = str(user_data.password)
    del new_data['password']
    new_user_data = UserAdd(**new_data)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {'status': 'OK', 'user': user}
