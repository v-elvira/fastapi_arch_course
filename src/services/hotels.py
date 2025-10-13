from datetime import date
from src.api.dependencies import PaginationParams
from src.exceptions import check_date_to_is_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_date(
            self,
            pagination: PaginationParams,
            title: str,
            location: str,
            date_from: date,
            date_to: date,
    ):
        per_page = pagination.per_page or 5
        check_date_to_is_after_date_from(date_from, date_to)
        return await self.db.hotels.get_filtered_by_date(date_from, date_to, location, title, per_page, pagination.start)

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def replace_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        hotel = await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        hotel = await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            return HotelNotFoundException
