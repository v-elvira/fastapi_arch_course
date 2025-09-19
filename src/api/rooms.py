from datetime import date
from fastapi import Body, APIRouter, HTTPException
from fastapi.params import Query, Path

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, Room, RoomAddBody, RoomWithRels
from src.utils.my_cache import my_redis_cache

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
@my_redis_cache()
async def get_rooms(
        db: DBDep,
        hotel_id: int = Path(description='Hotel id'),
        date_from: date = Query(example='2024-09-01'),
        date_to: date = Query(example='2025-12-01'),
) -> list[RoomWithRels]:
    return await db.rooms.get_filtered_by_date(hotel_id, date_from, date_to)


@router.get('/{hotel_id}/rooms/{room_id}')
@my_redis_cache(60)
async def get_room(hotel_id: int, room_id: int, db: DBDep) -> RoomWithRels | None:
    return await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)


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
                "quantity": 3,
                "facilities_ids": [2, 3]
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
    room_add_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(room_add_data)

    if room_data.facilities_ids:
        room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.room_facilities.add_bulk(room_facilities_data)

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

    await db.room_facilities.set_room_facilities(room_id, room_data.facilities_ids)
    del room_data.facilities_ids

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
    if room_data.facilities_ids is not None:
        await db.room_facilities.set_room_facilities(room_id, room_data.facilities_ids)
    del room_data.facilities_ids
    response = {'status': 'OK'}
    if any(x is not None for x in vars(room_data).values()):
        room = await db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        response['edited_room'] = room
    await db.session.commit()
    return response
