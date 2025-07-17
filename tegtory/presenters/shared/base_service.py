import logging
from typing import Any, ClassVar

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dishka.integrations.aiogram import setup_dishka

from tegtory.infrastructure import container
from tegtory.presenters.shared.bot import BotSingleton
from tegtory.presenters.shared.middlewares.auth import AuthMiddleware
from tegtory.presenters.shared.middlewares.executor import ExecutorMiddleware

logger = logging.getLogger(__name__)


class BaseService:
    bot_singleton: type[BotSingleton]
    message_middlewares: ClassVar[list] = [
        AuthMiddleware(),
        ExecutorMiddleware(),
    ]
    callback_middlewares: ClassVar[list] = [
        AuthMiddleware(),
        ExecutorMiddleware(),
    ]

    def __init__(self, bot_token: str | None = "") -> None:
        self.bot = self._get_bot(bot_token)
        self._dp: Any = None

    async def __call__(self, *args: tuple, **kwargs: dict) -> None:
        if not self.bot:
            return
        self.prepare_handlers()
        setup_dishka(container, self.dp, auto_inject=True)
        await self.dp.start_polling(self.bot, skip_updates=True)

    def prepare_handlers(self) -> None:
        pass

    @property
    def dp(self) -> Dispatcher:
        if isinstance(self._dp, Dispatcher):
            return self._dp
        dp = Dispatcher()
        self._register_middlewares(dp)

        self._dp = dp
        return dp

    @classmethod
    def _get_bot(cls, token: str | None = None) -> Bot | None:
        if not token:
            logger.error("No bot token provided for %s", cls.__name__)
            return None
        return cls.bot_singleton(
            token=token, default=DefaultBotProperties(parse_mode="Markdown")
        )

    def _register_middlewares(self, dp: Dispatcher) -> None:
        for middleware in self.message_middlewares:
            dp.message.middleware.register(middleware)
        for middleware in self.callback_middlewares:
            dp.callback_query.middleware.register(middleware)
