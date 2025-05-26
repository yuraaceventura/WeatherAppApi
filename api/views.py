import requests

from fastapi import APIRouter
import redis

from config.config import settings

r = redis.Redis(host=settings.redis.HOST,
                port=settings.redis.PORT,
                db=0, password=settings.redis.PASS,
                username=settings.redis.USER,
                decode_responses=True)

router = APIRouter()

api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


@router.post("/weather/{city}")
async def get_weather(city: str):
    cached_response = r.hmget(city, keys=["temperature", "humidity"])
    if all(cached_response) and cached_response[0] is not None:
        return {"temperature": cached_response[0], "humidity": cached_response[1]}

    request_url = api_url + city + "?key=" + settings.api.KEY
    response = requests.get(request_url).json()
    response = response["days"][0]
    temp = response["temp"]
    humidity = response["humidity"]

    r.hset(city, mapping={"temperature": f"{temp}", "humidity": f"{humidity}"})
    r.expire(city, 60)
    return {"temperature": f"{temp}", "humidity": f"{humidity}"}

