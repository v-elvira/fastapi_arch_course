from datetime import date
from fastapi import Body, APIRouter
from fastapi.params import Query, Path
from typing import Mapping

from src.api.dependencies import DBDep
from src.exceptions import (RoomNotFoundHTTPException, HotelNotFoundHTTPException,
                            RoomNotFoundException, HotelNotFoundException)

from src.schemas.rooms import RoomPatch, Room, RoomAddBody, RoomWithRels
from fastapi_cache.decorator import cache

from src.services.rooms import RoomService

router = APIRouter(prefix='/hotels', tags=['Rooms'])

# @router.get('/{hotel_id}/rooms')
# async def get_rooms(
#         db: DBDep,
#         hotel_id: int = Path(description='Hotel id'),
#         title: str | None = Query(None, description='Room title'),
#         description: str | None = Query(None, description='Room description'),
#         price: int | None = Query(None, description='Room price'),
#         quantity: int | None = Query(None, description='Room quantity'),
# ) -> list[Room]:
#     return await db.rooms.get_all(hotel_id, title, description, price, quantity)


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int = Path(description='Hotel id'),
    date_from: date = Query(examples=['2024-09-01']),
    date_to: date = Query(examples=['2025-12-01']),
) -> list[RoomWithRels]:
    return await RoomService(db).get_filtered_by_date(hotel_id, date_from, date_to)


@router.get('/{hotel_id}/rooms/{room_id}')
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep) -> RoomWithRels:
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, id=room_id)
    except RoomNotFoundException:
        RoomNotFoundHTTPException


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(hotel_id: int, room_id: int, db: DBDep) -> dict:
    await RoomService(db).delete_room(id=room_id, hotel_id=hotel_id)
    return {'status': 'OK'}


@router.post('/{hotel_id}/rooms')
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddBody = Body(
        openapi_examples={
            '1': {
                'summary': 'Люкс',
                'value': {
                    'title': 'Люкс',
                    'description': 'Люкс с видом на море',
                    'price': 1000,
                    'quantity': 3,
                    'facilities_ids': [2, 3],
                },
            },
            '2': {
                'summary': 'Стандарт',
                'value': {'title': 'Стандарт', 'description': 'Номер на двоих', 'price': 700, 'quantity': 12},
            },
        }
    ),
) -> dict:
    try:
        room = RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {'status': 'OK', 'data': room}


@router.put('/{hotel_id}/rooms/{room_id}')
async def replace_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddBody,
    db: DBDep,
) -> Mapping[str, Room | str]:
    try:
        room = await RoomService(db).replace_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        RoomNotFoundHTTPException
    return {'status': 'OK', 'new_room': room}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatch,
    db: DBDep,
) -> Mapping[str, Room | str]:
    try:
        room = RoomService(db).edit_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    response = {'status': 'OK'}
    if room:
        response['edited_room'] = room
    return response
