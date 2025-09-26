import pytest

from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker

# @pytest.mark.asyncio   # or add "asyncio_mode = auto" in pytest.ini for all functions
async def test_add_hotel():
    data = HotelAdd(title='Hotel 1', location='Main Street, 2')
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel = await db.hotels.add(data)
        print(f'{new_hotel=}')
        await db.commit()
