from datetime import date
from typing import List
from sqlalchemy import select, func

from src.database import engine
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel              # will be deleted when move to mappers in BaseRepository
    mapper = HotelDataMapper

    async def get_filtered_by_date(self,
                                   date_from: date,
                                   date_to: date,
                                   location: str | None,
                                   title: str | None,
                                   limit: int,
                                   offset: int,
    ) -> List[Hotel]:
        free_room_ids = room_ids_for_booking(date_from, date_to)
        free_hotel_ids = (
            select(RoomsORM.hotel_id)
            .distinct()
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(free_room_ids))
        )

        query = (
            select(HotelsORM)
            .select_from(HotelsORM)
            .filter(HotelsORM.id.in_(free_hotel_ids))
        )
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.lower()))
        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        print('HOTEL QUERY:\n', query.compile(bind=engine, compile_kwargs={"literal_binds": True}), '\n----')

        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]
