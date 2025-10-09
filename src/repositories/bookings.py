from datetime import date
from sqlalchemy import select

from src.exceptions import NoFreeRoomException
from src.models import RoomsORM
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import room_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = select(self.model).filter_by(date_from=date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):
        free_room_ids_q = room_ids_for_booking(booking_data.date_from, booking_data.date_to, hotel_id)
        query = (
            select(RoomsORM.id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(free_room_ids_q))
            .filter_by(id=booking_data.room_id)
        )
        result = await self.session.execute(query)
        if not result.scalars().all():
            raise NoFreeRoomException
        return await self.add(booking_data)
