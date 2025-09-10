from datetime import date
from fastapi import Body, APIRouter
from fastapi.params import Query

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel

from typing import List

router = APIRouter(prefix='/hotels', tags=['Hotels'])

@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description='Hotel title'),
        location: str | None = Query(None, description='Location fragment'),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
) -> List[Hotel]:
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_date(date_from, date_to, location, title, per_page, pagination.start)


@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int, db: DBDep) -> Hotel:
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep) -> dict:
    await db.hotels.delete(id=hotel_id)
    await db.session.commit()
    return {'status': 'OK'}


@router.post('')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(
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
# )) -> dict:   # PydanticSerializationError: Unable to serialize unknown type: <class 'src.models.hotels.HotelsORM'>
    hotel = await db.hotels.add(hotel_data)
    await db.session.commit()

    return {'status': 'OK', 'data': hotel}

@router.put('/{hotel_id}')
async def replace_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep,
) -> dict[str, Hotel | str]:
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.session.commit()
    return {'status': 'OK', 'new_hotel': hotel}


@router.patch('/{hotel_id}')
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
) -> dict[str, Hotel | str]:
    hotel = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.session.commit()
    return {'status': 'OK', 'edited_hotel': hotel}
