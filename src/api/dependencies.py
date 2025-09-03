import jwt
from fastapi import Query, Depends, Request
from pydantic import BaseModel, model_validator, computed_field
from typing import Annotated

from src.services.auth import AuthService

DEFAULT_PER_PAGE = 3

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=30)]

    @model_validator(mode='after')
    def default_per_page(self):
        if self.page > 1 and not self.per_page:
            self.per_page = DEFAULT_PER_PAGE
        return self

    @computed_field
    @property
    def start(self) -> int:
        if self.page > 1:
            return (self.page - 1) * self.per_page
        return 0

PaginationDep = Annotated[PaginationParams, Depends()]



def get_current_user_id(request: Request) -> int:
    access_token = request.cookies.get('access_token')
    data = AuthService().decode_token(access_token)
    return data['user_id']

UserIdDep = Annotated[int, Depends(get_current_user_id)]
