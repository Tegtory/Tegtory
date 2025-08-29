import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from aiogram import types

from tegtory.common.exceptions import FactoryRequiredError
from tegtory.domain.entities import Factory
from tegtory.domain.queries.factory import GetFactoryQuery, GetStorageQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure.query import QueryExecutor

logger = logging.getLogger(__name__)


def get_factory(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        event: types.Message | types.CallbackQuery,
        *args: tuple,
        **kwargs: dict,
    ) -> Any:
        if not event.from_user:
            return None
        factory = kwargs.pop("factory", await _get_factory(event.from_user.id))
        if not factory:
            raise FactoryRequiredError
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


async def _get_factory(user_id: int) -> Factory | None:
    result: Success[Factory] | Failure = await QueryExecutor().ask(
        GetFactoryQuery(factory_id=user_id)
    )
    if isinstance(result, Success):
        return result.data
    return None
