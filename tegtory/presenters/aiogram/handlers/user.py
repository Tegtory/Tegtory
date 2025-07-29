from aiogram import Router, types

from tegtory.common.settings import ASSETS_DIR
from tegtory.domain.entities import User
from tegtory.domain.entities.user import Wallet
from tegtory.domain.queries.user import WalletQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure import QueryExecutor
from tegtory.presenters.aiogram.filters.profile import (
    BalanceFilter,
    ProfileFilter,
)
from tegtory.presenters.aiogram.kb.other import balance_markup

router = Router()


@router.message(ProfileFilter())
async def user_info(message: types.Message, user: User) -> None:
    await message.answer_photo(
        types.FSInputFile(ASSETS_DIR / "passport.png"),
        caption=f"""\
🌟 *Паспорт {message.from_user.first_name if message.from_user else ""}*

""",
        reply_markup=balance_markup,
    )


@router.callback_query(BalanceFilter())
async def balance_info(
    call: types.CallbackQuery, user: User, query_executor: QueryExecutor
) -> None:
    result: Success[Wallet] | Failure = await query_executor.ask(
        WalletQuery(user_id=user.id)
    )
    if isinstance(result, Failure):
        return
    wallet = result.data
    await call.message.edit_caption(
        caption=f"""\
Ваш кошелек:

💲 *Баланс:* {wallet.money:,}
⚔️ *SC:* {wallet.stolar:,}
"""
    )
