from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload  # noqa F401

from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import room_ids_for_booking
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        free_room_ids = room_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))  # or joinedload
            .filter(self.model.id.in_(free_room_ids))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(item) for item in result.scalars().all()
        ]  # result.unique().. for joinedload

    async def get_one_with_rels(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).options(selectinload(self.model.facilities))
        result = await self.session.execute(query)
        try:
            model_item = result.scalars().one()
        except NoResultFound:
            return ObjectNotFoundException
        return RoomWithRelsDataMapper.map_to_domain_entity(model_item)

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
