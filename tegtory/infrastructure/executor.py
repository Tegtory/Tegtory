import logging
from collections.abc import Awaitable, Callable
from typing import Any, Self, cast, get_args

from tegtory.common.exceptions import AppError
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
            logger.info(f"Preparing {handler.__class__.__name__}")
            logger.debug(f"Bases: {handler.__orig_bases__}")
            logger.debug("=" * 50)
            args = get_args(handler.__orig_bases__[0])
            if not args:
                logger.critical("Error, while preparing handler")
                raise AppError(
                    f"Missing generic type in {handler.__class__.__name__}"
                )
            instance.register(args[0], handler)

        logger.info(f"{executor.__name__} Prepared")
