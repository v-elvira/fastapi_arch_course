from fastapi import Depends, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH, HotelGET
from typing import Annotated, List

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
        params: Annotated[HotelGET, Depends()]
) -> List[dict]:
    result = []
    for hotel in hotels:
        if params.id and hotel['id'] != params.id:
            continue
        if params.title and hotel['title'] != params.title:
            continue
        result.append(hotel)

    if params.per_page:
        return result[params.start: params.start + params.per_page]
    return result[params.start:]


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
                "name": "sochi_u_morya",
            }
        },
        "2": {
            "summary": "Дубай",
            "value": {
                "title": "Отель Дубай У фонтана",
                "name": "dubai_fountain",
            }
        }
    }
)) -> dict:
    global hotels
    hotels.append({'id': hotels[-1]['id']+1, 'title': hotel_data.title, 'name': hotel_data.name})
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
