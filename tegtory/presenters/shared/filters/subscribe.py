from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter

from tegtory.presenters.shared.bot import TegtorySingleton


async def is_subscribed(user_id: int) -> bool:
    chat_id = "@tegtory"
    try:
        chat_member = await TegtorySingleton().get_chat_member(
            chat_id, user_id
        )
        return chat_member.status != "left"
    except TelegramBadRequest:
        return False


class SubscribeFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if not message.from_user:
            return False
        return await is_subscribed(message.from_user.id)


class SubscribeFilterCallBack(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        return await is_subscribed(call.from_user.id)
