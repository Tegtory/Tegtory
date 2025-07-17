import logging
from collections.abc import Awaitable, Callable
from typing import Any, Self, cast

from tegtory.domain.results import Failure, Success

logger = logging.getLogger(__name__)


class BaseExecutor:
    _instance: Self | None = None
    handler_base_class: type

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance: Self = object.__new__(cls)
        return cast("Self", cls._instance)

    def __init__(self) -> None:
        if not hasattr(self, "handlers"):
            self.handlers: dict[
                type, Callable[[Any], Awaitable[Success | Failure]]
            ] = {}

    def register(
        self,
        command: type,
        handler: Callable[[Any], Awaitable[Success | Failure]],
    ) -> None:
        self.handlers[command] = handler


async def preparing_executors() -> None:
    from tegtory.infrastructure.di import container

    for executor in BaseExecutor.__subclasses__():
        logger.info(f"Preparing {executor.__name__}")
        instance = executor()
        children = executor.handler_base_class.__subclasses__()
        for child in children:
            handler: Any = await container.get(child)
            instance.register(handler.object_type, handler)
        logger.info(f"{executor.__name__} Prepared")
