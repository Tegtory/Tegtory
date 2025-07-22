import asyncio
import logging
from collections.abc import Callable
from typing import Any, ClassVar

from tegtory.domain.events import EventType
from tegtory.domain.interfaces import EventBus

logger = logging.getLogger(__name__)


class MemoryEventBus(EventBus):
    events: ClassVar[dict[Any, list[Callable]]] = {}

    @classmethod
    def subscribe(cls, callback: Callable, event_name: EventType) -> None:
        logger.debug(
            f"Subscribing to event {event_name} by {callback.__name__}"
        )
        if not cls.events.get(event_name):
            cls.events[event_name] = []
        cls.events[event_name].append(callback)

    @classmethod
    async def emit(cls, event: EventType, data: Any) -> None:
        logger.debug(
            f"Emitting event: {event} with data:\n"
            f"{cls._format_dict(data) if isinstance(data, dict) else data}"
        )
        for callback in cls.events.get(event, []):
            logger.debug(f"Emitting callback: {callback}")

            asyncio.create_task(cls._event_wrapper(callback, data))

    @classmethod
    def _format_dict(cls, data: dict) -> str:
        return "\n".join([f"{k} = {v}" for k, v in data.items()])

    @staticmethod
    async def _event_wrapper(call: Callable, data: Any) -> None:
        try:
            await call(data)
        except Exception as e:
            logger.error(f"Exception raised: {e} while executing {call}")
