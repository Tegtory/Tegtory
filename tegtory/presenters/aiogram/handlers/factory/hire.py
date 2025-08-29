from collections.abc import Callable
from typing import Any

from aiogram import F, Router, types

from tegtory.domain import entities, results
from tegtory.domain.commands import HireWorkerCommand
from tegtory.infrastructure import CommandExecutor
from tegtory.presenters.aiogram.images import Images
from tegtory.presenters.aiogram.kb import FactoryCB
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.aiogram.utils import cache, get_factory

router = Router()


@router.callback_query(F.data == FactoryCB.workers)
@get_factory
@cache(Images.factory_hire, types.FSInputFile(Images.factory_hire))
async def workers_page(
    call: types.CallbackQuery,
    factory: entities.Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    sent = await call.message.edit_media(
        media=types.InputMediaPhoto(
            caption=msg.workers_page.format(
                factory.workers, factory.hire_available, factory.hire_price
            ),
            media=cached,
        ),
        reply_markup=kb.hire_markup,
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == FactoryCB.hire)
@get_factory
async def hire(
    call: types.CallbackQuery, cmd_executor: CommandExecutor
) -> None:
    result = await cmd_executor.execute(
        HireWorkerCommand(user_id=call.from_user.id)
    )
    markup = kb.failed_hire_markup
    if isinstance(result, results.Success):
        await workers_page(call)
        return

    await call.message.edit_caption(caption=result.reason, reply_markup=markup)
