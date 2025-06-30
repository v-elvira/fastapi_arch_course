from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM

class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsORM)
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

        hotels = result.scalars().all()
        return hotels