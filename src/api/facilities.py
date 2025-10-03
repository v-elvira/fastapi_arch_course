from typing import List
from fastapi import Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix='/facilities', tags=['Facilities'])

@router.get('')
@cache(expire=100)
async def get_facilities(
        db: DBDep,
) -> List[Facility]:
    return await db.facilities.get_all()

@router.post('', status_code=201)
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body(),
) -> dict[str, str | Facility]:
    facility = await db.facilities.add(facility_data)
    if not facility:
        raise HTTPException(status_code=400, detail='Failed to create facility')
    await db.commit()

    test_task.delay()

    return {'status': 'OK', 'data': facility}
