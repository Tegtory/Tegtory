import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    BOT_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    USER_MICROSERVICE_URL: str
    USER_MICROSERVICE_KEY: str


DELIVERY_MIN_DISTANT = 10
DEFAULT_TAX_LIMIT = 50000
HIRE_PRICE = 370

TAX_LIMIT: int = int(os.environ.get("TAX_LIMIT", DEFAULT_TAX_LIMIT))
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"

settings = Settings()
