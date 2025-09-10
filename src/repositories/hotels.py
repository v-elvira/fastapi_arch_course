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

        # if title or location:
        #    free_hotel_ids = free_hotel_ids.join(HotelsORM, free_hotel_ids.c.hotel_id == HotelsORM.id)

        ## sqlalchemy.exc.ProgrammingError: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <
        ## class 'asyncpg.exceptions.UndefinedTableError'>: missing FROM - clause entry for table "anon_1"
        ##  ---- OK without it

        if title:
            free_hotel_ids = free_hotel_ids.filter(func.lower(HotelsORM.title).contains(title.lower()))
        if location:
            free_hotel_ids = free_hotel_ids.filter(func.lower(HotelsORM.location).contains(location.lower()))
        free_hotel_ids = (free_hotel_ids
                 .limit(limit)
                 .offset(offset)
                 )
        print('HOTEL QUERY:\n', free_hotel_ids.compile(bind=engine, compile_kwargs={"literal_binds": True}), '\n----')

        return await self.get_filtered(HotelsORM.id.in_(free_hotel_ids))
