from typing import Any, Self, cast

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession


class BotSingleton(Bot):
    _instance: Self | None = None

    def __new__(
        cls: type[Self],
        token: str | None = None,
        session: BaseSession | None = None,
        default: DefaultBotProperties | None = None,
        **kwargs: Any,
    ) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cast("Self", cls._instance)


class TegtorySingleton(BotSingleton):
    pass


class MynoxSingleton(BotSingleton):
    pass
