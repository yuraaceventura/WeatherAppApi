import redis
import uvicorn
from fastapi import FastAPI
from config.config import settings
from api.views import router as api_router

r = redis.Redis(host=settings.redis.HOST, port=settings.redis.PORT, db=0, password=settings.redis.PASS, decode_responses=True)

app = FastAPI()
app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)