from typing import List
from fastapi import Body, APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix='/facilities', tags=['Facilities'])

@router.get('')
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
    await db.session.commit()
    return {'status': 'OK', 'data': facility}
