import dataclasses
from collections.abc import Callable

from tegtory.domain.interfaces.eventbus import EventBus


class DependencyRequired:
    pass


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
