import pytest

from src.database import Base, engine_null_pool
from src.config import settings


@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'
    print('Checked TEST mode')

@pytest.fixture(scope='session', autouse=True)
async def async_main(check_test_mode):
    print('Main fixture applying')

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
