import pytest
from httpx import AsyncClient, ASGITransport

from src.database import Base, engine_null_pool
from src.config import settings
from src.main import app

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
