from aiogram import types
from aiogram.filters import BaseFilter

from tegtory.presenters.aiogram.kb.callbacks import FactoryCB


class OpenFactoryFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return message.text.lower() in ["фабрика", "ф", "af,hbrf", "a"]
        return False


class ChooseProductFilter(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        return (
            call.data.lower() == FactoryCB.work_yourself
            or call.data.lower() == FactoryCB.start
        )


class ChooseTimeToWorkFilter(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        return call.data.startswith(f"{FactoryCB.choose_time}:")


class StartYourselfFactoryFilter(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        if call.data:
            return call.data.lower().startswith(f"{FactoryCB.work_yourself}:")
        return False


class StartFactoryFilter(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        if call.data:
            return call.data.lower().startswith(f"{FactoryCB.start}:")
        return False
