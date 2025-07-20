import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tegtory.infrastructure import CommandExecutor, QueryExecutor

logger = logging.getLogger(__name__)


class ExecutorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["cmd_executor"] = CommandExecutor()
        data["query_executor"] = QueryExecutor()
        return await handler(event, data)
