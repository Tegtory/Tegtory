from typing import Any

from aiogram import F, Router, types

from tegtory.domain import entities, results
from tegtory.domain.commands import UpgradeStorageCommand
from tegtory.infrastructure import CommandExecutor
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.kb.callbacks import FactoryCB
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.shared.utils import (
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
    result = get_storage_page_text(storage)
    await call.message.edit_caption(
        caption=result, reply_markup=kb.storage_markup
    )


@router.callback_query(F.data == FactoryCB.upgrade_storage)
@get_factory
async def upgrade_storage(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    cmd_executor: CommandExecutor,
) -> Any:
    result = await cmd_executor.execute(
        UpgradeStorageCommand(
            factory_id=factory.id,
            storage=factory.storage,
            user_money=user.money,
            user_id=user.id,
        )
    )
    if isinstance(result, results.Failure):
        return await call.answer(result.reason, show_alert=True)
    await open_storage(call)


def get_storage_page_text(storage: entities.Storage) -> str:
    result = msg.storage_title
    for product, amount in storage.products.items():
        result += msg.storage_products.format(product.name, amount)
    result += msg.storage_footer.format(storage.max_stock)
    return result
