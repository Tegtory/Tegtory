import logging

from aiogram import Router, types
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from tegtory.common.exceptions import (
    DuringWorkError,
    FactoryRequiredError,
    NotEnoughPointsError,
)
from tegtory.presenters.aiogram.kb import factory as kb_factory
from tegtory.presenters.aiogram.messages import factory as factory_msg

router = Router()
logger = logging.getLogger(__name__)


@router.error(ExceptionTypeFilter(NotEnoughPointsError, DuringWorkError))
async def not_enough_points(event: ErrorEvent) -> None:
    if not event.update.callback_query:
        return
    if hasattr(event.exception, "message"):
        await event.update.callback_query.answer(
            event.exception.message or "Вы не можете выполнить это действие",
            show_alert=True,
        )


@router.error(ExceptionTypeFilter(FactoryRequiredError))
async def factory_required_handler(event: ErrorEvent) -> None:
    user: types.User | None = None
    message: types.Message | types.InaccessibleMessage | None = None
    if event.update.message:
        user = event.update.message.from_user
        message = event.update.message
    elif event.update.callback_query:
        user = event.update.callback_query.from_user
        message = event.update.callback_query.message
    if not user:
        logger.error("У События нет пользователя")
        return
    logger.info(f"Пользователь {user.id} не имеет фабрики")
    if message:
        await message.answer(
            factory_msg.need_to_create, reply_markup=kb_factory.create_markup
        )
    return
