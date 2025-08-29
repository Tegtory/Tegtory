from typing import Any

from aiogram import F, Router, types

from tegtory.domain import entities, results
from tegtory.domain.commands import UpgradeStorageCommand
from tegtory.infrastructure import CommandExecutor
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.kb.callbacks import FactoryCB
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.aiogram.utils import (
    get_factory,
    get_storage_from_factory,
)

router = Router()


@router.callback_query(F.data == FactoryCB.storage)
@get_factory
@get_storage_from_factory
async def open_storage(
    call: types.CallbackQuery, storage: entities.Storage
) -> None:
    await call.message.edit_caption(
        caption=msg.get_storage_page_text(storage),
        reply_markup=kb.storage_markup,
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
async def upgrade_storage(
    call: types.CallbackQuery,
    cmd_executor: CommandExecutor,
) -> Any:
    result = await cmd_executor.execute(
        UpgradeStorageCommand(user_id=call.from_user.id)
    )
    if isinstance(result, results.Failure):
        return await call.answer(result.reason, show_alert=True)
    await open_storage(call)
