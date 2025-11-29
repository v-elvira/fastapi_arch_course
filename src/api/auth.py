from fastapi import APIRouter, Response, status, Depends

from src.api.dependencies import UserIdDep, DBDep, get_token
from src.exceptions import WrongEmailPasswordException, WrongEmailPasswordHTTPException, \
    UserExistsException, UserExistsHTTPException
from src.schemas.users import UserRequestAdd, User
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['User auth'])  # , dependencies=...) for the whole route Deps


@router.post('/login')
async def login_user(user_data: UserRequestAdd, db: DBDep, response: Response) -> dict:
    try:
        access_token = await AuthService(db).login_user(user_data)
    except WrongEmailPasswordException as ex:
        raise WrongEmailPasswordHTTPException from ex

    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRequestAdd, db: DBDep) -> dict[str, str | User]:
    try:
        user = await AuthService(db).register(user_data)
    except UserExistsException:
        raise UserExistsHTTPException
    return {'status': 'OK', 'user': user}


@router.get('/me', summary="Get me ✅")
async def get_me(user_id: UserIdDep, db: DBDep) -> User | None:
    return await AuthService(db).get_user(user_id)


@router.post('/logout')
async def logout_user(response: Response, token: str = Depends(get_token)) -> dict:
    response.delete_cookie('access_token')
    return {'status': 'ok'}
