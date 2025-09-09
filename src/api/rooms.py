from datetime import date
from fastapi import Body, APIRouter, HTTPException
from fastapi.params import Query, Path

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, Room, RoomAddBody

from typing import List

router = APIRouter(prefix='/hotels', tags=['Rooms'])

# @router.get('/{hotel_id}/rooms')
# async def get_rooms(
#         db: DBDep,
#         hotel_id: int = Path(description='Hotel id'),
#         title: str | None = Query(None, description='Room title'),
#         description: str | None = Query(None, description='Room description'),
#         price: int | None = Query(None, description='Room price'),
#         quantity: int | None = Query(None, description='Room quantity'),
# ) -> List[Room]:
#     return await db.rooms.get_all(hotel_id, title, description, price, quantity)

@router.get('/{hotel_id}/rooms')
async def get_rooms(
        db: DBDep,
        hotel_id: int = Path(description='Hotel id'),
        date_from: date = Query(example='2024-09-01'),
        date_to: date = Query(example='2025-12-01'),
): #-> List[Room]:
    return await db.rooms.get_filtered_by_date(hotel_id, date_from, date_to)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int, db: DBDep) -> Room | None:
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(hotel_id: int, room_id: int, db: DBDep) -> dict:
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.session.commit()
    return {'status': 'OK'}


@router.post('/{hotel_id}/rooms')
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddBody = Body(
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
    if not await db.hotels.get_one_or_none(id=hotel_id):
        raise HTTPException(status_code=404, detail='Hotel not found. Failed to create room')
    room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(room_data)
    await db.session.commit()

    return {'status': 'OK', 'data': room}

@router.put('/{hotel_id}/rooms/{room_id}')
async def replace_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddBody,
        db: DBDep,
) -> dict[str, Room | str]:
    if not await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id):
        raise HTTPException(status_code=404, detail=f'No room with id {room_id} found in this hotel')
    room = await db.rooms.edit(room_data, id=room_id)
    await db.session.commit()
    return {'status': 'OK', 'new_room': room}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatch,
        db: DBDep,
) -> dict[str, Room | str]:
    if not await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id):
        raise HTTPException(status_code=404, detail=f'No room with id {room_id} found in this hotel')
    room = await db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.session.commit()
    return {'status': 'OK', 'edited_room': room}
