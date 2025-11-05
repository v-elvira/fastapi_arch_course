from pydantic import Field, model_validator
from src.schemas.common import CommonBaseModel


class HotelAdd(CommonBaseModel):
    title: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=5, max_length=200)


class Hotel(HotelAdd):
    id: int


class HotelPatch(CommonBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    location: str | None = Field(default=None, min_length=5, max_length=200)

    @model_validator(mode='after')
    def all_empty_not_allowed(self):
        if not self.title and not self.location:
            raise ValueError('Empty title and location')
        return self
