from src.schemas.common import CommonBaseModel

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

class RoomPatch(CommonBaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None
