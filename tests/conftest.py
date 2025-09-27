import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.config import settings
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.main import app
from src.utils.db_manager import DBManager

from src.models import *                            # for Base.metadata to be seen. But worked OK without it (?)

@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'
    print('Checked TEST mode')

@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    print('Main fixture applying')

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope='session', autouse=True)
async def fill_database(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open('tests/mock_hotels.json', encoding='utf-8') as hotels_file:
            data = json.load(hotels_file)
            await db.hotels.add_bulk([HotelAdd.model_validate(item) for item in data])

        with open('tests/mock_rooms.json', encoding='utf-8') as rooms_file:
            data = json.load(rooms_file)
            await db.rooms.add_bulk([RoomAdd.model_validate(item) for item in data])

        await db.commit()


@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(
            '/auth/register',
            json={
                'email': 'me@mail.ru',
                'password': 'me',
            },
        )
        assert response.status_code == 201
