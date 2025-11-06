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


## ORIGINAL course variant:

# def rooms_ids_for_booking(
#     date_from: date,
#     date_to: date,
#     hotel_id: int | None = None,
# ) -> Select:
#     rooms_count = (
#         select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
#         .select_from(BookingsOrm)
#         .filter(
#             BookingsOrm.date_from <= date_to,
#             BookingsOrm.date_to >= date_from,
#         )
#         .group_by(BookingsOrm.room_id)
#         .cte(name="rooms_count")
#     )
#
#     rooms_left_table = (
#         select(
#             RoomsOrm.id.label("room_id"),
#             (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
#         )
#         .select_from(RoomsOrm)
#         .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
#         .cte(name="rooms_left_table")
#     )
#
#     rooms_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)
#     if hotel_id is not None:
#         rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)
#
#     rooms_ids_for_hotel_subq: Subquery = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")
#
#     rooms_ids_to_get = (
#         select(rooms_left_table.c.room_id)
#         .select_from(rooms_left_table)
#         .filter(
#             rooms_left_table.c.rooms_left > 0,
#             rooms_left_table.c.room_id.in_(rooms_ids_for_hotel_subq),  # type: ignore
#         )
#     )
#     return rooms_ids_to_get
