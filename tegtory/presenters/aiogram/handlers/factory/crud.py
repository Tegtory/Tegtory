from collections.abc import Callable
from typing import Any

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from tegtory.domain import entities, results
from tegtory.domain.commands import CreateFactoryCommand, UpgradeFactoryCommand
from tegtory.infrastructure import CommandExecutor
from tegtory.presenters.aiogram.handlers.factory.main import open_factory
from tegtory.presenters.aiogram.images import Images
from tegtory.presenters.aiogram.kb import FactoryCB
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.aiogram.states import factory as states
from tegtory.presenters.shared.utils import cache, get_factory

router = Router()


@router.callback_query(F.data == FactoryCB.create)
async def create_factory_callback(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    await call.message.edit_text(msg.set_name, reply_markup=None)
    await state.set_state(states.Create.name)


@router.message(StateFilter(states.Create.name))
async def finish_create_factory_handler(
    message: types.Message, state: FSMContext, cmd_executor: CommandExecutor
) -> Any:
    await message.delete()
    result = await cmd_executor.execute(
        CreateFactoryCommand(id=message.from_user.id, name=str(message.text))
    )
    if isinstance(result, results.Success):
        await state.clear()
        return await open_factory(message)
    await message.answer(msg.unique_name)


@router.callback_query(F.data == FactoryCB.upgrade)
@get_factory
@cache(Images.factory_upgrade, types.FSInputFile(Images.factory_upgrade))
async def upgrade_factory(
    call: types.CallbackQuery,
    factory: entities.Factory,
    cached: Any,
    cache_func: Callable,
) -> None:
    try:
        sent = await call.message.edit_media(
            media=types.InputMediaPhoto(
                caption=msg.upgrade_page.format(
                    factory.level, factory.upgrade_price
                ),
                media=cached,
            ),
            reply_markup=kb.upgrade_markup,
        )
        if sent.photo:
            cache_func(sent.photo[-1].file_id)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == FactoryCB.upgrade_conf)
@get_factory
async def try_to_upgrade_factory(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    cmd_executor: CommandExecutor,
) -> Any:
    result = await cmd_executor.execute(
        UpgradeFactoryCommand(
            factory_id=factory.id,
            factory_upgrade_price=factory.upgrade_price,
            user_id=user.id,
            user_money=user.money,
        )
    )

    if isinstance(result, results.Success):
        return await upgrade_factory(call)
    await call.message.edit_caption(
        caption=result.reason, reply_markup=kb.failed_upgrade_markup
    )
