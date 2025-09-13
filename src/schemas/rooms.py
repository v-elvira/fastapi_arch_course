from src.schemas.common import CommonBaseModel
from src.schemas.facilities import Facility


class RoomAddBody(CommonBaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

class RoomAdd(CommonBaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

class RoomWithRels(Room):
    facilities: list[Facility]

class RoomPatch(CommonBaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None
