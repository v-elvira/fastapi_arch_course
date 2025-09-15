from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword

class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_item = result.scalars().one_or_none()
        if model_item is None:
            return None
        return UserWithHashedPassword.model_validate(model_item)
