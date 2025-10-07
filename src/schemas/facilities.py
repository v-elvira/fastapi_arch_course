from pydantic import Field
from src.schemas.common import CommonBaseModel


class FacilityAdd(CommonBaseModel):
    title: str = Field(max_length=100)


class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(CommonBaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
