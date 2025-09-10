from datetime import date
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        free_room_ids = room_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsORM.id.in_(free_room_ids))



    # async def get_all(self, hotel_id, title, description, price, quantity):
    #     query = select(self.model)
    #     if hotel_id:
    #         query = query.filter(self.model.hotel_id == hotel_id)
    #     if title:
    #         query = query.filter(func.lower(self.model.title).contains(title.lower()))
    #     if description:
    #         query = query.filter(func.lower(self.model.description).contains(description.lower()))
    #     if price:
    #         query = query.filter(self.model.price <= price)
    #     if quantity:
    #         query = query.filter(self.model.quantity >= quantity)
    #
    #     print(query.compile(compile_kwargs={'literal_binds': True}))
    #     result = await self.session.execute(query)
    #
    #     rooms = [self.schema.model_validate(item) for item in result.scalars().all()]
    #     return rooms
