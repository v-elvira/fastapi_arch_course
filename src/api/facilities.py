import json
from typing import List
from fastapi import Body, APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd

from src.init import redis_manager

router = APIRouter(prefix='/facilities', tags=['Facilities'])

@router.get('')
async def get_facilities(
        db: DBDep,
) -> List[Facility]:
    facilities_from_cache = await redis_manager.get('facilities')
    if not facilities_from_cache:
        print('MAKING facilities DB QUERY')
        facilities = await db.facilities.get_all()
        facilities_dict = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_dict)
        print(facilities_json, type(facilities_json))
        await redis_manager.set('facilities', facilities_json, 10)
        return facilities
    else:
        return json.loads(facilities_from_cache)

@router.post('', status_code=201)
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body(),
) -> dict[str, str | Facility]:
    facility = await db.facilities.add(facility_data)
    if not facility:
        raise HTTPException(status_code=400, detail='Failed to create facility')
    await db.session.commit()
    return {'status': 'OK', 'data': facility}
