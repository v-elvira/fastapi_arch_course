from sqlalchemy import select, insert
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, model_data: BaseModel):
        add_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        print(add_stmt.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

