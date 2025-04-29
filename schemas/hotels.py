from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = Field(None)
