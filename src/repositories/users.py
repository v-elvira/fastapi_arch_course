from src.repositories.base import BaseRepository
from src.models.users import UserORM
from src.schemas.users import User

class UsersRepository(BaseRepository):
    model = UserORM
    schema = User
