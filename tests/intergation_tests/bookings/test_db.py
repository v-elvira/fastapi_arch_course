from datetime import date
from src.schemas.bookings import BookingAdd, BookingPatch


async def test_booking_crud(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    data = BookingAdd(
        date_from=date(year=2024, month=12, day=1),
        date_to=date(year=2024, month=12, day=10),
        room_id=room_id,
        user_id=user_id,
        price=1000,
    )
    booking = await db.bookings.add(data)
    assert booking
    booking_id = booking.id
    await db.commit()

    added_booking = await db.bookings.get_one_or_none(id=booking_id)
    assert added_booking
    assert data.model_dump() == added_booking.model_dump(exclude={'id'})

    edited = await db.bookings.edit(model_data=BookingPatch(price=777), exclude_unset=True, id=booking_id)
    assert edited.price == 777
    assert edited.id == booking_id

    await db.bookings.delete(id=booking_id)
    deleted = await db.bookings.get_one_or_none(id=booking_id)
    assert not deleted
    await db.commit()
