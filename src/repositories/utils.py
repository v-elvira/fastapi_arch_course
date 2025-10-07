from datetime import date
from sqlalchemy import select, func
from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM


def room_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    booked = (
        select(BookingsORM.room_id, func.count('*').label('rooms_booked'))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name='booked')
    )

    free_rooms = select(
        RoomsORM.id.label('room_id'), (RoomsORM.quantity - func.coalesce(booked.c.rooms_booked, 0)).label('free_count')
    ).select_from(RoomsORM)
    if hotel_id:
        free_rooms = free_rooms.filter_by(hotel_id=hotel_id)
    free_rooms = free_rooms.outerjoin(booked, RoomsORM.id == booked.c.room_id).cte(name='free_rooms')

    room_ids = select(free_rooms.c.room_id).select_from(free_rooms).filter(free_rooms.c.free_count > 0)
    # print(room_ids.compile(bind=engine, compile_kwargs={"literal_binds": True}))
    return room_ids
