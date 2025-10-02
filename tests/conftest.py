import json
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport

from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.config import settings
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.main import app
from src.utils.db_manager import DBManager
from src.api.dependencies import get_db

from src.models import *                            # for Base.metadata to be seen. But worked OK without it (?)

@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'
    print('Checked TEST mode')

async def get_db_null_poll():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope='function')   # default scope
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_poll():
        yield db


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    print('Setup DB fixture applying')

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope='session', autouse=True)
async def fill_database(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        with open('tests/mock_hotels.json', encoding='utf-8') as hotels_file:
            data = json.load(hotels_file)
            await db_.hotels.add_bulk([HotelAdd.model_validate(item) for item in data])

        with open('tests/mock_rooms.json', encoding='utf-8') as rooms_file:
            data = json.load(rooms_file)
            await db_.rooms.add_bulk([RoomAdd.model_validate(item) for item in data])

        await db_.commit()


@pytest.fixture(scope='session')
async def client():
    app.dependency_overrides[get_db] = get_db_null_poll
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest.fixture(scope='session', autouse=True)
async def register_user(client, setup_database):
    response = await client.post(
        '/auth/register',
        json={
            'email': 'me@mail.ru',
            'password': 'me',
        },
    )
    assert response.status_code == 201
