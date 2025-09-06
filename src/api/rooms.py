from fastapi import Body, APIRouter, HTTPException
from fastapi.params import Query, Path

from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, Room, RoomAddBody

from src.database import async_session_maker

from typing import List

router = APIRouter(prefix='/hotels', tags=['Rooms'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(
        hotel_id: int = Path(description='Hotel id'),
        title: str | None = Query(None, description='Room title'),
        description: str | None = Query(None, description='Room description'),
        price: int | None = Query(None, description='Room price'),
        quantity: int | None = Query(None, description='Room quantity'),
) -> List[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id, title, description, price, quantity)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int) -> Room | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(hotel_id: int, room_id: int) -> dict:
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {'status': 'OK'}


@router.post('/{hotel_id}/rooms')
async def create_room(hotel_id: int, room_data: RoomAddBody = Body(
    openapi_examples={
        "1": {
            "summary": "Люкс",
            "value": {
                "title": "Люкс",
                "description": "Люкс с видом на море",
                "price": 1000,
                "quantity": 3
            }
        },
        "2": {
            "summary": "Стандарт",
            "value": {
                "title": "Стандарт",
                "description": "Номер на двоих",
                "price": 700,
                "quantity": 12
            }
        }
    }
)) -> dict:
    async with (async_session_maker() as session):
        if not await HotelsRepository(session).get_one_or_none(id=hotel_id):
            raise HTTPException(status_code=404, detail='Hotel not found. Failed to create room')
        room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {'status': 'OK', 'data': room}

@router.put('/{hotel_id}/rooms/{room_id}')
async def replace_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddBody,
) -> dict[str, Room | str]:
    async with async_session_maker() as session:
        if not await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id):
            raise HTTPException(status_code=404, detail=f'No room with id {room_id} found in this hotel')
        room = await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {'status': 'OK', 'new_room': room}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatch,
) -> dict[str, Room | str]:
    async with async_session_maker() as session:
        if not await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id):
            raise HTTPException(status_code=404, detail=f'No room with id {room_id} found in this hotel')
        room = await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {'status': 'OK', 'edited_room': room}
