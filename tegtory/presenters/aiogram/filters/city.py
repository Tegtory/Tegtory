from aiogram import types
from aiogram.filters import BaseFilter


class CityFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return message.text.lower() in ["город", "city", "ujhjl", "г", "u"]
        return False
