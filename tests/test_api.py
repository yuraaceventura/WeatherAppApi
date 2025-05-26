import pytest
from unittest.mock import patch
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from api.views import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
@patch("api.views.r")
async def test_get_weather_from_cache(mock_redis):
    mock_redis.hmget.return_value = ["20.5", "50"]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/weather/London")

    assert response.status_code == 200
    assert response.json() == {"temperature": "20.5", "humidity": "50"}
    mock_redis.hmget.assert_called_once_with("London", keys=["temperature", "humidity"])
    mock_redis.hset.assert_not_called()

@pytest.mark.asyncio
@patch("api.views.r")
@patch("api.views.requests.get")
async def test_get_weather_from_api(mock_requests_get, mock_redis):
    mock_redis.hmget.return_value = [None, None]

    mock_requests_get.return_value.json.return_value = {
        "days": [{"temp": 20.5, "humidity": 50}]
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/weather/Berlin")

    assert response.status_code == 200
    assert response.json() == {"temperature": "20.5", "humidity": "50"}

    mock_redis.hset.assert_called_once_with(
        "Berlin", mapping={"temperature": "20.5", "humidity": "50"}
    )
    mock_redis.expire.assert_called_once_with("Berlin", 60)
