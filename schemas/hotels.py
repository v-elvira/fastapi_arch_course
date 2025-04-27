from pydantic import BaseModel, Field, model_validator, computed_field

DEFAULT_PER_PAGE = 3

class Hotel(BaseModel):
    title: str
    name: str

class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = Field(None)

class HotelGET(BaseModel):
    id: int | None = None
    title: str | None = Field(default=None)
    page: int = Field(default=1, ge=1)
    per_page: int | None = Field(None, ge=1)

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
