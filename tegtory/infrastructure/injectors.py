from collections.abc import Callable

from tegtory.domain.events import EventType
from tegtory.domain.interfaces import EventBus

_pending_subscriptions = []


def on_event(event_name: EventType) -> Callable:
    def decorator(func: Callable) -> Callable:
        _pending_subscriptions.append((event_name, func))
        return func

    return decorator


def subscribe_all(event_bus: EventBus) -> None:
    for event_name, func in _pending_subscriptions:
        event_bus.subscribe(func, event_name)
