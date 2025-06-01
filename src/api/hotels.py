from fastapi import Body, APIRouter
from fastapi.params import Query

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

from src.database import async_session_maker
# from src.database import engine
from src.models.hotels import HotelsORM

from typing import List

hotels = [
    {'id': 1, 'title': 'Hotel one', 'name': 'one'},
    {'id': 2, 'title': 'Sochi', 'name': 'sochi'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

router = APIRouter(prefix='/hotels', tags=['Hotels'])

@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description='Id'),
        title: str | None = Query(None, description='Hotel title'),
) -> List[dict]:
    result = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        result.append(hotel)

    if pagination.per_page:
        return result[pagination.start: pagination.start + pagination.per_page]
    return result[pagination.start:]


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
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
)) -> dict:
    async with (async_session_maker() as session):
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        # # for DEBUG:
        # print(f'1: {add_hotel_stmt}')
        # # INSERT INTO hotels (title, location) VALUES (:title, :location)
        # print(f'2: {add_hotel_stmt.compile()}')
        # # INSERT INTO hotels (title, location) VALUES (:title, :location)
        #
        # print(f'3: {add_hotel_stmt.compile(engine)}')  # engine for DB dialect (RETURNING in postgres)
        # # INSERT INTO hotels (title, location) VALUES ($1::VARCHAR, $2::VARCHAR) RETURNING hotels.id
        #
        # print(f'4: {add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True})}')
        # # INSERT INTO hotels (title, location) VALUES ('Отель Сочи 5 звезд у моря', 'Sochi, Main, 6') RETURNING hotels.id

        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


@router.put('/{hotel_id}')
async def replace_hotel(
        hotel_id: int,
        hotel_data: Hotel,
) -> dict:
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = hotel_data.name
            hotel['title'] = hotel_data.title
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}


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
