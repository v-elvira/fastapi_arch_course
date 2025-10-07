from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL)  # , echo=True) to log every query
# # Can be replaced with following for tests (or use dependency_overrides in conftest.py):
# engin_params = {'poolclass': NullPool} if settings.MODE == 'TEST' else {}
# engine = create_async_engine(settings.DB_URL, **engin_params)

engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
