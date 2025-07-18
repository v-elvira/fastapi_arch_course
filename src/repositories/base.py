from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from src.schemas.common import CommonBaseModel
from src.database import Base

class BaseRepository:
    model = Base
    schema = CommonBaseModel

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result_db = await self.session.execute(query)
        #result = [self.schema.model_validate(item, from_attributes=True) for item in result_orm.scalars().all()]  # ok

        # Without "from_attributes"=True will be error 'Input should be a valid dictionary or instance of Hotel'
        # Default from_attributes=True is moved to schemas (model_config = ConfigDict(...))

        result = [self.schema.model_validate(item) for item in result_db.scalars().all()]
        return result

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_item = result.scalars().one_or_none()
        if model_item is None:
            return None
        return self.schema.model_validate(model_item)

    async def add(self, model_data: CommonBaseModel):
        add_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        print(add_stmt.compile(compile_kwargs={'literal_binds': True}))
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError:
            return
        return self.schema.model_validate(result.scalars().one())

    async def edit(self, model_data: CommonBaseModel, exclude_unset=False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**model_data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        print(update_stmt.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(update_stmt)
        return self.schema.model_validate(result.scalars().one())

    async def delete(self, **filter_by) -> None:
        del_stmt = delete(self.model).filter_by(**filter_by)
        print(del_stmt.compile(compile_kwargs={'literal_binds': True}))
        await self.session.execute(del_stmt)
