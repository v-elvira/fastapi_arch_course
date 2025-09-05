from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
print(sys.path) # was already there? # +2 times in the end (not in __main__ => on import?)

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.config import settings

print(f'DB_NAME: {settings.DB_NAME}')

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)

@app.get('/', name='Home page')
async def index() -> dict:
    return {'Hello': 42}



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True, port=8000)
