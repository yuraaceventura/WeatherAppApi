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
    if response := r.hmget(city, keys=["temp", "humidity"]) :
        if response[0] is not None:
            return response
    request_url = api_url + city + "?key=" + settings.api.KEY
    response = requests.get(request_url)
    response = response.json()
    response = response["days"][0]
    temp = response["temp"]
    humidity = response["humidity"]
    r.hset(city, mapping={"temp": f"temperature: {str(temp)}", "humidity": f"humidity:{str(humidity)}"})
    r.expire(city, 60)
    return r.hmget(city, keys=["temp", "humidity"])
