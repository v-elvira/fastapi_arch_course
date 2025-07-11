from fastapi import Body, APIRouter
from fastapi.params import Query

from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

from src.database import async_session_maker

from typing import List

router = APIRouter(prefix='/hotels', tags=['Hotels'])

@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Hotel title'),
        location: str | None = Query(None, description='Location fragment'),
):  # -> List[Hotel]: (will be casted to Hotel schema (with to id))
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(location, title, per_page, pagination.start)


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int) -> dict:
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.post('')
async def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        "1": {
            "summary": "Сочи",
            "value": {
                "title": "Отель Сочи 5 звезд у моря",
                "location": "Sochi, Main, 5",
            }
        },
        "2": {
            "summary": "Дубай",
            "value": {
                "title": "Отель Дубай У фонтана",
                "location": "Dubai, Fountain, 1",
            }
        }
    }
)):
# )) -> dict:   # PydanticSerializationError: Unable to serialize unknown type: <class 'src.models.hotels.HotelsORM'>
    async with (async_session_maker() as session):
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': hotel}

@router.put('/{hotel_id}')
async def replace_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK', 'new_hotel': hotel}


@router.patch('/{hotel_id}')
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
) -> dict:
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.name:
                hotel['name'] = hotel_data.name
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}
