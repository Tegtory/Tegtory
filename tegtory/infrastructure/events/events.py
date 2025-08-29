from typing import Any

from tegtory.domain.interfaces import EventBus
from tegtory.domain.use_cases.base import EventBased
from tegtory.infrastructure.di import container
from tegtory.infrastructure.utils import get_children


async def subscribe_events() -> None:
    event_bus = await container.get(EventBus)
    events = get_subscribed_events(EventBased)

    for cls, subscribers in events:
        instance = await container.get(cls)
        for sub in subscribers:
            event_bus.subscribe(getattr(instance, sub.__name__), sub.__event__)


def get_subscribed_events(klass: type[EventBased]) -> list[list[Any]]:
    events = []
    for cls in get_children(klass):
        cls_typing: EventBased = cls
        events.append([cls_typing, cls_typing.get_subscribers()])
    return events
