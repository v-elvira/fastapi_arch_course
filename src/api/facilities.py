from typing import List
from fastapi import Body, APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix='/facilities', tags=['Facilities'])


@router.get('')
@cache(expire=100)
async def get_facilities(
    db: DBDep,
) -> List[Facility]:
    return await FacilityService(db).get_facilities()


@router.post('', status_code=201)
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
) -> dict[str, str | Facility]:
    facility = await FacilityService(db).create_facility(facility_data)
    return {'status': 'OK', 'data': facility}
