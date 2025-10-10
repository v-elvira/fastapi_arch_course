from fastapi import APIRouter, Response, status, HTTPException

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectExistsException
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['User auth'])  # , dependencies=...) for the whole route Deps


@router.post('/login')
async def login_user(user_data: UserRequestAdd, db: DBDep, response: Response) -> dict:
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user or not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong email/password')
    access_token = AuthService().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRequestAdd, db: DBDep) -> dict[str, str | User]:
    new_data = UserRequestAdd.model_dump(user_data)
    new_data['hashed_password'] = AuthService().hash_password(user_data.password)
    del new_data['password']
    new_user_data = UserAdd(**new_data)
    try:
        user = await db.users.add(new_user_data)
    except ObjectExistsException:
        raise HTTPException(status_code=409, detail=f'User with email {user_data.email} already exists')
    await db.commit()
    return {'status': 'OK', 'user': user}


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep) -> User | None:
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post('/logout')
async def logout_user(response: Response) -> dict:
    response.delete_cookie('access_token')
    return {'status': 'ok'}
