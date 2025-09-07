from fastapi import Query, Depends, Request, HTTPException
from pydantic import BaseModel, model_validator, computed_field
from typing import Annotated

from src.services.auth import AuthService
from src.database import async_session_maker
from src.utils.db_manager import DBManager


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

def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='No token provided')
    return token

def get_current_user_id(token: Annotated[str, Depends(get_token)]) -> int:
# def get_current_user_id(token: str = Depends(get_token)) -> int:  # same, ok
    data = AuthService().decode_token(token)
    return data['user_id']

UserIdDep = Annotated[int, Depends(get_current_user_id)]

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
