from datetime import date
from typing import List
from sqlalchemy import select, func

from src.database import engine
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_filtered_by_date(self, date_from: date, date_to: date) -> List[Hotel]:
        free_room_ids = room_ids_for_booking(date_from, date_to)
        free_hotel_ids = (
            select(RoomsORM.hotel_id)
            .distinct()
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(free_room_ids))
        )
        print(free_hotel_ids.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(HotelsORM.id.in_(free_hotel_ids))

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