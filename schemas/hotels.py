from fastapi import Query
from pydantic import BaseModel, Field, model_validator, computed_field
from typing import Annotated

DEFAULT_PER_PAGE = 3

class Hotel(BaseModel):
    title: str
    name: str

class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = Field(None)

class HotelGET(BaseModel):
    id: Annotated[int | None, Query(None)]
    title: Annotated[str | None, Query(default=None)]
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1)]

    @model_validator(mode='after')
    def default_per_page(self):
        if self.page > 1 and not self.per_page:
            self.per_page = DEFAULT_PER_PAGE

    @computed_field
    @property
    def start(self) -> int:
        if self.page > 1:
            return (self.page - 1) * self.per_page
        return 0
