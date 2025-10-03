from typing import List
from fastapi import Body, APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddBody, BookingPatch

router = APIRouter(prefix='/bookings', tags=['Bookings'])

@router.post('', status_code=201)
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddBody = Body(),
) -> dict[str, str | Booking]:
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f'No room with id {booking_data.room_id}')
    full_booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(full_booking_data, hotel_id=room.hotel_id)
    if not booking:
        raise HTTPException(status_code=400, detail='Failed to create booking')
    await db.commit()
    return {'status': 'OK', 'data': booking}


@router.get('')
async def get_all_bookings(
        db: DBDep,
) -> List[Booking]:
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(
        db: DBDep,
        user_id: UserIdDep
) -> List[Booking]:
    return await db.bookings.get_filtered(user_id=user_id)

@router.patch('/{booking_id}')
async def edit_booking(
        booking_id: int,
        booking_data: BookingPatch,
        db: DBDep,
        user_id: UserIdDep,
) -> dict[str, Booking | str]:
    booking = await db.bookings.get_one_or_none(id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    if booking.user_id != user_id:
        raise HTTPException(status_code=401, detail='User has no right to edit this booking')
    booking = await db.bookings.edit(booking_data, exclude_unset=True, id=booking_id)
    await db.commit()
    return {'status': 'OK', 'edited_booking': booking}
