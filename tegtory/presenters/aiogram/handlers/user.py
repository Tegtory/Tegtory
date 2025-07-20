from aiogram import Router, types

from tegtory.common.settings import ASSETS_DIR
from tegtory.domain.entities import User
from tegtory.presenters.aiogram.filters.profile import ProfileFilter
from tegtory.presenters.aiogram.messages.user import format_user

router = Router()


@router.message(ProfileFilter())
async def user_info(message: types.Message, user: User) -> None:
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=format_user(user),
    )
