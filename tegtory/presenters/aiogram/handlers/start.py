from aiogram import F, Router, types
from aiogram.filters import CommandStart

from ..kb.legacy import menu_reply
from ..messages.main import guide_message, welcome_message

router = Router()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        welcome_message.format(message.from_user.first_name),
        reply_markup=menu_reply,
    )


@router.message(F.text.lower() == "помощь")
async def help_message(message: types.Message) -> None:
    await message.answer(guide_message)
