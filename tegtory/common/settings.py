from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    BOT_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""

    USER_URL: str
    USER_KEY: str

    WALLET_URL: str
    WALLET_KEY: str
    WALLET_VALUE: str

    @property
    def redis_url(self) -> str:
        return (
            f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}"
        )

    @property
    def money_metadata(self) -> tuple[tuple[str, str]]:
        return ((self.WALLET_KEY, self.WALLET_VALUE),)


HIRE_PRICE = 370

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"
settings = Settings()
