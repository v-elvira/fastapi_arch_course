from fastapi import Query, Depends
from pydantic import BaseModel, model_validator, computed_field
from typing import Annotated

DEFAULT_PER_PAGE = 3

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=30)]

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

PaginationDep = Annotated[PaginationParams, Depends()]
