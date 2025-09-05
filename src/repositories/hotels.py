from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.lower()))
        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)

        hotels = [self.schema.model_validate(item) for item in result.scalars().all()]
        return hotels