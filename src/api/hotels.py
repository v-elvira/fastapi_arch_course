from fastapi import Body, APIRouter
from fastapi.params import Query

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

from src.database import async_session_maker
from src.database import engine
from src.models.hotels import HotelsORM

from typing import List

router = APIRouter(prefix='/hotels', tags=['Hotels'])

@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Hotel title'),
        location: str | None = Query(None, description='Location fragment'),
) -> List[Hotel]:
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.lower()))
        query = (query
                 .limit(per_page)
                 .offset(pagination.start)
                 )
        print(f'Q: {query.compile(engine, compile_kwargs = {'literal_binds': True})}')
        #Q: SELECT hotels.id, hotels.title, hotels.location FROM hotels +- WHERE ... +- AND ...

        result = await session.execute(query)
        # print(f'1: {result}')              # <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f5da2034b90>
        # print(f'2: {result.all()}')            # [(<src.models.hotels.HotelsORM object at 0x7fab83f1f380>,), ...
        # print(f'3: {result.scalars()}')        # <sqlalchemy.engine.result.ScalarResult object at 0x7f5da2024140>
        # print(f'4: {result.scalars().all()}')    # [<src.models.hotels.HotelsORM object at 0x7f8b4987f050>, ...
        # WILL BE EMPTY IF called twice
    hotels = result.scalars().all()
    return hotels


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
