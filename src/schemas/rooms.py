from pydantic import Field, model_validator
from src.schemas.common import CommonBaseModel
from src.schemas.facilities import Facility


class RoomAddBody(CommonBaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(CommonBaseModel):
    hotel_id: int
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatch(CommonBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None

    @model_validator(mode='after')
    def all_empty_not_allowed(self):
        if not any((self.title, self.description, self.price, self.quantity, self.facilities_ids)):
            raise ValueError('All empty fields are not allowed')
        return self
