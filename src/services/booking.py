from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    BookingNotFoundException,
    NotAllowedException,
    check_date_to_is_after_date_from,
)
from src.schemas.bookings import BookingAddBody, BookingAdd, BookingPatch
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, booking_data: BookingAddBody):
        check_date_to_is_after_date_from(
            booking_data.date_from, booking_data.date_to
        )  # HTTPError is not good in Service
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        full_booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        booking = await self.db.bookings.add_booking(full_booking_data, hotel_id=room.hotel_id)
        await self.db.commit()
        return booking

    async def edit_booking(self, booking_id: int, booking_data: BookingPatch, user_id: int):
        booking = await self.db.bookings.get_one_or_none(id=booking_id)
        if not booking:
            raise BookingNotFoundException
        if booking.user_id != user_id:
            raise NotAllowedException
        booking = await self.db.bookings.edit(booking_data, exclude_unset=True, id=booking_id)
        await self.db.commit()
        return booking
