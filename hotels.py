from fastapi import Query, Body, APIRouter
from typing import List

hotels = [
    {'id': 1, 'title': 'Hotel one', 'name': 'one'},
    {'id': 2, 'title': 'Sochi', 'name': 'sochi'},
]


router = APIRouter(prefix='/hotels', tags=['Hotels'])

@router.get('')
async def get_hotels(
        id: int | None = Query(None, description='Hotel id'),
        title: str | None = Query(None, description='Hotel title'),
) -> List[dict]:
    result = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        result.append(hotel)
    return result


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.post('')
async def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(),
) -> dict:
    global hotels
    hotels.append({'id': hotels[-1]['id']+1, 'title': title, 'name': name})
    return {'status': 'OK'}


@router.put('/{hotel_id}')
async def replace_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
) -> dict:
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = name
            hotel['title'] = title
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}


@router.patch('/{hotel_id}')
async def edit_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
) -> dict:
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if name:
                hotel['name'] = name
            if title:
                hotel['title'] = title
            return {'status': 'OK'}
    return {'status': 'Hotel not found'}
