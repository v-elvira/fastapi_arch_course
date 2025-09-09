from datetime import date
from sqlalchemy import select, func
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        booked = (
            select(BookingsORM.room_id, func.count('*').label('rooms_booked'))
            .select_from(BookingsORM)
            .filter(
                BookingsORM.date_from <= date_to,
                BookingsORM.date_to >= date_from
            )
            .group_by(BookingsORM.room_id)
            .cte(name='booked')
        )
        free_rooms = (
            select(
                RoomsORM.id.label('room_id'),
                (RoomsORM.quantity - func.coalesce(booked.c.rooms_booked, 0)).label('free_count')
            )
            .select_from(RoomsORM)
            .outerjoin(booked, RoomsORM.id == booked.c.room_id)
            .cte(name='free_rooms')
        )
        query = select('*').select_from(free_rooms).filter(free_rooms.c.free_count > 0)
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()  # -> List[int] (free room_id-s list) (DB SQL -> 2 columns: room_id, free_count)

'''
WITH booked AS 
    (SELECT bookings.room_id AS room_id, count('*') AS rooms_booked 
    FROM bookings 
    WHERE bookings.date_from <= '2025-12-01' AND bookings.date_to >= '2025-09-01' GROUP BY bookings.room_id), 
free_rooms AS 
    (SELECT rooms.id AS room_id, rooms.quantity - coalesce(booked.rooms_booked, 0) AS free_count 
    FROM rooms LEFT OUTER JOIN booked ON rooms.id = booked.room_id)
SELECT * 
FROM free_rooms 
WHERE free_rooms.free_count > 0
'''



    # async def get_all(self, hotel_id, title, description, price, quantity):
    #     query = select(self.model)
    #     if hotel_id:
    #         query = query.filter(self.model.hotel_id == hotel_id)
    #     if title:
    #         query = query.filter(func.lower(self.model.title).contains(title.lower()))
    #     if description:
    #         query = query.filter(func.lower(self.model.description).contains(description.lower()))
    #     if price:
    #         query = query.filter(self.model.price <= price)
    #     if quantity:
    #         query = query.filter(self.model.quantity >= quantity)
    #
    #     print(query.compile(compile_kwargs={'literal_binds': True}))
    #     result = await self.session.execute(query)
    #
    #     rooms = [self.schema.model_validate(item) for item in result.scalars().all()]
    #     return rooms
