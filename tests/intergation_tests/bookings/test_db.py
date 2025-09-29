from datetime import date
from src.schemas.bookings import BookingAdd

async def test_add_booking(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    data = BookingAdd(
        date_from=date(year=2024, month=12, day=1),
        date_to=date(year=2024, month=12, day=10),
        room_id=room_id,
        user_id=user_id,
        price=1000,
    )
    await db.bookings.add(data)
    await db.commit()
