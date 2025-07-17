from aiogram import types
from aiogram.filters import BaseFilter


class LeaderboardFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return message.text.lower() in [
                "таблица лидеров",
                "зал славы",
                "тл",
                "зс",
                "nk",
                "pc",
            ]
        return False
