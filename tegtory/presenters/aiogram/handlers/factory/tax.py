from collections.abc import Callable
from typing import Any

from aiogram import F, Router, types

from tegtory.domain import entities, results
from tegtory.domain.commands import PayTaxCommand
from tegtory.infrastructure import CommandExecutor
from tegtory.presenters.aiogram.images import Images
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.kb.callbacks import FactoryCB
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.aiogram.utils import cache, get_factory

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
async def pay_tax(
    call: types.CallbackQuery,
    cmd_executor: CommandExecutor,
) -> None:
    result = await cmd_executor.execute(
        PayTaxCommand(user_id=call.from_user.id)
    )
    if isinstance(result, results.Success):
        text = msg.tax_page.format(0)
    else:
        text = result.reason
    if str(call.message.caption).strip() == text.strip():
        return
    await call.message.edit_caption(caption=text, reply_markup=kb.tax_markup)
