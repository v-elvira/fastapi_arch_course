# ruff: noqa: E402
import asyncio
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# from fastapi_cache.backends.inmemory import InMemoryBackend
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
print(sys.path)  # was already there? # +2 times in the end (not in __main__ => on import?)

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.dependencies import get_db
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.config import settings

from src.init import redis_manager

print(f'DB_NAME: {settings.DB_NAME}')

# logging.basicConfig(
#     filename='logfile.txt',
#     level=logging.DEBUG,
#     format='%(levelname)s %(asctime)s "%(message)s" %(lineno)d %(funcName)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )
logging.basicConfig(level=logging.INFO)


async def send_daily_checkins():
    async for db in get_db():
        bookings = await db.bookings.get_booking_with_today_checkin()
        print(f'Regular async task: {bookings=}')


async def run_regular_sender():
    while True:
        print('Regular hello')  # OK
        await send_daily_checkins()  # first real DB connection attempt on FastAPI startup will be in this function
        await asyncio.sleep(777)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on FastAPI startup
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix='fastapi-cache')
    logging.info("FastAPI cache initialized")
    asyncio.create_task(run_regular_sender())
    yield
    # on FastAPI shutdown
    await redis_manager.close()


# if settings.MODE == 'TEST':                   # -> mock.patch for cache in conftest.py
#     #FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get('/', name='Home page')
async def index() -> dict:
    return {'Hello': 42}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', reload=True, port=8000)
    # if --network=host while starting docker, default host (localhost) is OK
