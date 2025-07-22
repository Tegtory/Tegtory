from collections.abc import Callable
from typing import Any, Protocol, Self

from tegtory.domain.events import EventType


class EventBus(Protocol):
    _instance: Self | None = None

    def __new__(cls) -> Any:
        if not cls._instance:
            cls._instance: Self = object.__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, callback: Callable, event_name: EventType) -> None:
        pass

    @classmethod
    async def emit(cls, event: EventType, data: Any) -> None:
        pass
