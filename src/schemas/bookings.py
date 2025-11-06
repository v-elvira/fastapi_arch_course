from datetime import date
from src.schemas.common import CommonBaseModel


class BookingAddBody(CommonBaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BookingAddBody):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int


class BookingPatch(CommonBaseModel):
    price: int
