from collections.abc import Callable
from typing import Any

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection

from tegtory.domain.events import EventType
from tegtory.domain.interfaces import EventBus


def inject(func: Callable) -> Any:
    def container_getter(
        _args: tuple[Any, ...], _kwargs: dict[str, Any]
    ) -> AsyncContainer:
        return container

    from .di import container

    return wrap_injection(
        func=func, container_getter=container_getter, is_async=True
    )


_pending_subscriptions = []


def on_event(event_name: EventType) -> Callable:
    def decorator(func: Callable) -> Callable:
        _pending_subscriptions.append((event_name, func))
        return func

    return decorator


def subscribe_all(event_bus: EventBus) -> None:
    for event_name, func in _pending_subscriptions:
        event_bus.subscribe(func, event_name)
