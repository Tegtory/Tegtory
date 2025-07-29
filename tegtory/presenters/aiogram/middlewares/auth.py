import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from tegtory.domain.commands import RegisterUserCommand
from tegtory.domain.entities import User
from tegtory.domain.queries import UserQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure import CommandExecutor, QueryExecutor

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not hasattr(event, "from_user") or not isinstance(
            event.from_user, types.User
        ):
            return None
        user = await self._get_user(event.from_user.id)
        if not user:
            user = await self._create_user(event.from_user)
        data["user"] = user
        return await handler(event, data)

    @staticmethod
    async def _create_user(user: types.User) -> User | None:
        logger.info(f"Registering user {user.id} - {user.username}")
        start = time.time()
        result: Success[User] | Failure = await CommandExecutor().execute(
            RegisterUserCommand(
                user_id=user.id,
                name=user.first_name,
                username=user.username or "none",
            )
        )
        end = time.time()
        logger.info(f"Время регистрации: {((end - start) * 1000)}")
        if isinstance(result, Success):
            return result.data
        logger.error(result.reason)
        return None

    @staticmethod
    async def _get_user(user_id: int) -> User | None:
        res: Success[User] | Failure = await QueryExecutor().ask(
            UserQuery(user_id=user_id)
        )
        if isinstance(res, Success):
            return res.data
        return None
