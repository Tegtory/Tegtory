import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from aiogram import types

from tegtory.domain.entities import Factory
from tegtory.domain.queries.factory import GetFactoryQuery, GetStorageQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure.query import QueryExecutor
from tegtory.presenters.aiogram.kb import factory as kb_factory
from tegtory.presenters.aiogram.messages import factory as factory_msg

logger = logging.getLogger(__name__)


def get_factory(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        *args: tuple,
        **kwargs: dict,
    ) -> Any:
        if not event.from_user:
            return
        factory = kwargs.pop("factory", await _get_factory(event.from_user.id))
        if not factory:
            await factory_required_handler(event)
            return
        return await func(event, *args, factory=factory, **kwargs)

    return wrapper


def get_storage_from_factory(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: tuple, **kwargs: Any) -> Any:
        factory: Factory = kwargs.pop("factory")
        result = await QueryExecutor().ask(
            GetStorageQuery(factory_id=factory.id)
        )
        if isinstance(result, Success):
            return await func(*args, storage=result.data, **kwargs)

    return wrapper


def get_event_message(
    event: types.Message | types.CallbackQuery | None,
) -> types.Message | types.InaccessibleMessage | None:
    return (
        event.message
        if isinstance(event, types.CallbackQuery) and event.message is not None
        else event
        if isinstance(event, types.Message)
        else None
    )


async def _get_factory(user_id: int) -> Factory | None:
    result: Success[Factory] | Failure = await QueryExecutor().ask(
        GetFactoryQuery(factory_id=user_id)
    )
    if isinstance(result, Success):
        return result.data
    return None


async def factory_required_handler(
    event: types.CallbackQuery | types.Message,
) -> None:
    if not event.from_user:
        logger.error("У События нет пользователя")
        return None
    logger.info(f"Пользователь {event.from_user.id} не имеет фабрики")
    message = get_event_message(event)
    if message:
        await message.answer(
            factory_msg.need_to_create, reply_markup=kb_factory.create_markup
        )
    return None
