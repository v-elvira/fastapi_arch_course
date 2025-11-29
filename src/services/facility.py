from src.exceptions import ObjectExistsException, UnknownFacilityError
from src.models import FacilitiesORM
from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, facility_data: FacilityAdd):
        if await self.db.facilities.get_filtered(**facility_data.model_dump()):
            raise ObjectExistsException
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()
        return facility

    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def check_facilities_ids(self, ids):
        if not ids:
            return
        existing_facilities = await self.db.facilities.get_filtered(FacilitiesORM.id.in_(ids))
        if len(existing_facilities) < len(ids):
            raise UnknownFacilityError
