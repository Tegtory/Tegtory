from aiogram import Router, types

from tegtory.common.settings import ASSETS_DIR
from tegtory.domain.entities import User
from tegtory.presenters.aiogram.filters.profile import ProfileFilter

router = Router()


@router.message(ProfileFilter())
async def user_info(message: types.Message, user: User) -> None:
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=f"""\
🌟 *Паспорт {message.from_user.first_name}*

💲 *Баланс:* {user.money:,}
⚔️ *SC:* {user.stolar:,}
""",
    )
