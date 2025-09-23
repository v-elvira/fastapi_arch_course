from datetime import date
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingDataMapper

class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = select(self.model).filter_by(date_from=date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]
