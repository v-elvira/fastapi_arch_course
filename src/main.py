from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
print(sys.path) # was already there? # +2 times in the end (not in __main__ => on import?)

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.config import settings

from src.init import redis_manager

print(f'DB_NAME: {settings.DB_NAME}')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on FastAPI startup
    await redis_manager.connect()
    yield
    # on FastAPI shutdown
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

@app.get('/', name='Home page')
async def index() -> dict:
    return {'Hello': 42}



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True, port=8000)
