from datetime import date
from fastapi import Body, APIRouter
from fastapi.params import Query
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, check_date_to_is_after_date_from
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel

from typing import List

from src.services.hotels import HotelService

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('')
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description='Hotel title'),
    location: str | None = Query(None, description='Location fragment'),
    date_from: date = Query(examples=['2024-08-01']),
    date_to: date = Query(examples=['2024-08-10']),
) -> List[Hotel]:
    return await HotelService(db).get_filtered_by_date(pagination, title, location, date_from, date_to)


@router.get('/{hotel_id}')
@cache(30)
async def get_hotel(hotel_id: int, db: DBDep) -> Hotel:
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep) -> dict:
    await HotelService(db).delete_hotel(hotel_id)
    return {'status': 'OK'}


@router.post('')
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {
                    'title': 'Отель Сочи 5 звезд у моря',
                    'location': 'Sochi, Main, 5',
                },
            },
            '2': {
                'summary': 'Дубай',
                'value': {
                    'title': 'Отель Дубай У фонтана',
                    'location': 'Dubai, Fountain, 1',
                },
            },
        }
    ),
) -> dict:
    # )) -> dict:   # PydanticSerializationError: Unable to serialize unknown type: <class 'src.models.hotels.HotelsORM'>
    hotel = await HotelService(db).add_hotel(hotel_data)

    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}')
async def replace_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
) -> dict[str, Hotel | str]:
    hotel = await HotelService(db).replace_hotel(hotel_id, hotel_data)
    return {'status': 'OK', 'new_hotel': hotel}


@router.patch('/{hotel_id}')
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
) -> dict[str, Hotel | str]:
    hotel = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'OK', 'edited_hotel': hotel}
