from datetime import date
from fastapi import Body, APIRouter
from fastapi.params import Query
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import HotelNotFoundHTTPException, HotelNotFoundException, \
    ObjectExistsException, HotelExistsHTTPException, FailedToDeleteHTTPException
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
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10'),
) -> List[Hotel]:
    return await HotelService(db).get_filtered_by_date(pagination, title, location, date_from, date_to)


@router.get('/{hotel_id}')
@cache(30)
async def get_hotel(hotel_id: int, db: DBDep) -> Hotel:
    try:
        return await HotelService(db).get_hotel_with_check(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep) -> dict:
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except IntegrityError:
        raise FailedToDeleteHTTPException

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
    try:
        hotel = await HotelService(db).add_hotel(hotel_data)
    except ObjectExistsException:
        raise HotelExistsHTTPException

    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}')
async def replace_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
) -> dict[str, Hotel | str]:
    try:
        hotel = await HotelService(db).replace_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {'status': 'OK', 'new_hotel': hotel}


@router.patch('/{hotel_id}')
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
) -> dict[str, Hotel | str]:
    try:
        hotel = await HotelService(db).edit_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {'status': 'OK', 'edited_hotel': hotel}
