from aiogram import types
from aiogram.filters import BaseFilter


class ProfileFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return message.text.lower() in [
                "профиль",
                "я",
                "z",
                "паспорт",
                "gfcgjhn",
            ]
        return False
