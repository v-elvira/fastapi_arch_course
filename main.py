from fastapi import FastAPI
from hotels import router as router_hotels
import uvicorn

app = FastAPI()
app.include_router(router_hotels)

@app.get('/', name='Home page')
async def index() -> dict:
    return {'Hello': 42}



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True, port=8000)
