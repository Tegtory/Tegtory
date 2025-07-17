import dataclasses
from collections.abc import Callable
from functools import wraps
from types import MethodType
from typing import Any

from tegtory.common.exceptions import AppError
from tegtory.domain.interfaces.eventbus import EventBus


class DependencyRequired:
    pass


class SafeCall:
    def __getattribute__(self, i: str) -> Any:
        obj = object.__getattribute__(self, i)
        return (
            obj if not isinstance(obj, MethodType) else self._get_wrapper(obj)
        )

    @staticmethod
    def _get_wrapper(obj: Callable) -> Callable:
        @wraps(obj)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any:
            try:
                return await obj(*args, **kwargs)
            except AppError as e:
                return e.message

        return wrapper


@dataclasses.dataclass(frozen=True)
class EventBased(DependencyRequired):
    event_bus: EventBus

    @classmethod
    def get_subscribers(cls) -> list[Callable]:
        subs = []
        for attr in filter(
            lambda x: hasattr(getattr(cls, x), "__event__"), dir(cls)
        ):
            subs.append(getattr(cls, attr))
        return subs
