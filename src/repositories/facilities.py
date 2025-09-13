from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, new_facilities: list[int]):
        old_facilities = {f.facility_id for f in await self.get_filtered(room_id=room_id)}
        to_remove = old_facilities - set(new_facilities)
        to_add = set(new_facilities) - old_facilities
        if to_add:
            data_to_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in to_add]
            await self.add_bulk(data_to_add)
        if to_remove:
            await self.delete(RoomsFacilitiesOrm.facility_id.in_(to_remove), room_id=room_id)
