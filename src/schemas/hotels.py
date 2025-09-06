from pydantic import Field
from src.schemas.common import CommonBaseModel


class HotelAdd(CommonBaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

class HotelPatch(CommonBaseModel):
    title: str | None = None
    location: str | None = Field(None)
