from collections.abc import Callable
from typing import Any

from aiogram import F, Router, types

from domain import entities, results
from domain.commands import PayTaxCommand
from infrastructure import CommandExecutor
from presenters.aiogram.images import Images
from presenters.aiogram.kb import factory as kb
from presenters.aiogram.kb.callbacks import FactoryCB
from presenters.aiogram.messages import factory as msg
from presenters.shared.utils import cache, get_factory

router = Router()


@router.callback_query(F.data == FactoryCB.tax)
@get_factory
@cache(Images.factory_tax, types.FSInputFile(Images.factory_tax))
async def tax_page(
    call: types.CallbackQuery,
    factory: entities.Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(
            caption=msg.tax_page.format(factory.tax), media=cached
        ),
        reply_markup=kb.tax_markup,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.pay_tax)
@get_factory
async def pay_tax(
    call: types.CallbackQuery,
    factory: entities.Factory,
    user: entities.User,
    cmd_executor: CommandExecutor,
) -> None:
    result = await cmd_executor.execute(
        PayTaxCommand(
            user_id=user.id,
            user_money=user.money,
            factory_id=factory.id,
            factory_tax=factory.tax,
        )
    )
    if isinstance(result, results.Success):
        text = msg.tax_page.format(0)
    else:
        text = result.reason
    if str(call.message.caption).strip() == text.strip():
        return
    await call.message.edit_caption(caption=text, reply_markup=kb.tax_markup)
