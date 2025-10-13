from src.exceptions import check_date_to_is_after_date_from, ObjectNotFoundException, RoomNotFoundException, \
    RoomNotFoundHTTPException, HotelNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomWithRels, RoomAddBody, RoomAdd, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_date(self, hotel_id, date_from, date_to):
        check_date_to_is_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_date(hotel_id, date_from, date_to)


    async def get_room(self, hotel_id: int, room_id: int) -> RoomWithRels:
        return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)


    async def delete_room(self, room_id: int, hotel_id: int):
        if not await self.db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id):
            raise RoomNotFoundHTTPException
        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()


    async def create_room(self, hotel_id: int, room_data: RoomAddBody):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        room_add_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(room_add_data)

        if room_data.facilities_ids:
            room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
            await self.db.room_facilities.add_bulk(room_facilities_data)

        await self.db.commit()
        return room


    async def replace_room(self, hotel_id: int, room_id: int, room_data: RoomAddBody):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(hotel_id=hotel_id, room_id=room_id)

        await self.db.room_facilities.set_room_facilities(room_id, room_data.facilities_ids)
        del room_data.facilities_ids

        room = await self.db.rooms.edit(room_data, id=room_id)
        await self.db.commit()
        return room


    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomPatch):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(hotel_id=hotel_id, room_id=room_id)

        if room_data.facilities_ids is not None:
            await self.db.room_facilities.set_room_facilities(room_id, room_data.facilities_ids)
        del room_data.facilities_ids

        edited_room = None
        if any(x is not None for x in vars(room_data).values()):
            edited_room = await self.db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await self.db.commit()
        return edited_room


    async def get_room_with_check(self, hotel_id: int, room_id: int):
        try:
            self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        except ObjectNotFoundException:
            return RoomNotFoundException
