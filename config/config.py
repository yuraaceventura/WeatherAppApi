import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = pathlib.Path(__file__).parent.absolute()
ENV_FILE_PATH = BASE_DIR / '.env'

class SetiingsBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="ignore"
    )

class RedisSettings(SetiingsBase):
    USER:str
    PORT:str
    HOST:str
    PASS:str

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class WeatherApiSettings(SetiingsBase):
    KEY:str

    model_config = SettingsConfigDict(env_prefix="API_")


class Settings(BaseSettings):

    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: WeatherApiSettings = Field(default_factory=WeatherApiSettings)


settings = Settings()
