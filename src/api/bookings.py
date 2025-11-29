from typing import List
from fastapi import Body, APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAddBody, BookingPatch
from src.exceptions import (
    NoFreeRoomException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    NoFreeRoomHTTPException,
    BookingNotFoundException,
    BookingNotFoundHTTPException,
    NotAllowedException,
    BookingEditingNotAllowedHTTPException,
)
from src.services.booking import BookingService

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.post('', status_code=201)
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddBody = Body(),
) -> dict[str, str | Booking]:
    try:
        booking = await BookingService(db).create_booking(user_id=user_id, booking_data=booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoFreeRoomException:
        raise NoFreeRoomHTTPException
    return {'status': 'OK', 'data': booking}


@router.get('')
async def get_all_bookings(
    db: DBDep,
) -> List[Booking]:
    return await BookingService(db).get_all_bookings()


@router.get('/me')
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> List[Booking]:
    return await BookingService(db).get_user_bookings(user_id=user_id)


@router.patch('/{booking_id}')
async def edit_booking(
    booking_id: int,
    booking_data: BookingPatch,
    db: DBDep,
    user_id: UserIdDep,
) -> dict[str, Booking | str]:
    try:
        booking = await BookingService(db).edit_booking(booking_id, booking_data, user_id)
    except BookingNotFoundException:
        raise BookingNotFoundHTTPException
    except NotAllowedException:
        raise BookingEditingNotAllowedHTTPException
    return {'status': 'OK', 'edited_booking': booking}
