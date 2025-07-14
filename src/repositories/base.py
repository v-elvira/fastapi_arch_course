from sqlalchemy import select, insert, update, delete
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
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, model_data: BaseModel):
        add_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        print(add_stmt.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def edit(self, model_data: BaseModel, exclude_unset=False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**model_data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        print(update_stmt.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(update_stmt)
        return result.scalars().one_or_none()

    async def delete(self, **filter_by) -> None:
        del_stmt = delete(self.model).filter_by(**filter_by)
        print(del_stmt.compile(compile_kwargs={'literal_binds': True}))
        await self.session.execute(del_stmt)
