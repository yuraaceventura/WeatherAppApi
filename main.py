import redis
from fastapi import FastAPI

from config.config import settings

from api.views import router as api_router


r = redis.Redis(host=settings.redis.HOST, port=settings.redis.PORT, db=0, password=settings.redis.PASS, username=settings.redis.USER, decode_responses=True)

app = FastAPI()
app.include_router(api_router)


