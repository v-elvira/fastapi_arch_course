import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text

from src.config import settings

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
# session = async_session_maker()
# await session.execute('...')

async def temp_func():
    async with engine.begin() as conn:
        result = await conn.execute(text('SELECT version()'))
        print(result.fetchone())

asyncio.run(temp_func())
