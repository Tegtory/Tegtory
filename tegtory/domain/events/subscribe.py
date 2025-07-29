from collections.abc import Callable

from tegtory.domain.events.event_types import EventType


def on_event(event: EventType) -> Callable:
    def decorator(func: Callable) -> Callable:
        setattr(func, "__event__", event)
        return func

    return decorator
