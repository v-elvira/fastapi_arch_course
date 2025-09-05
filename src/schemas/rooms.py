from src.schemas.common import CommonBaseModel

class RoomAddBody(CommonBaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomAdd(RoomAddBody):
    hotel_id: int

class Room(RoomAdd):
    id: int

class RoomPATCH(CommonBaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
