from aiogram import types
from aiogram.filters import BaseFilter

from tegtory.presenters.aiogram.kb.callbacks import OtherCB


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


class BalanceFilter(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        if call.data:
            return call.data == OtherCB.balance
        return False
