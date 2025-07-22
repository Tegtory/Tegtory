import dataclasses
from typing import Any

import pytest

from tegtory.domain.events import EventType, on_event
from tegtory.domain.use_cases.base import EventBased


@dataclasses.dataclass(frozen=True)
class MockEventBased(EventBased):
    @on_event(EventType.SubtractMoney)
    def sub_money(self, event: Any) -> None:
        pass


@pytest.mark.asyncio
async def test_on_event() -> None:
    decorator = on_event(EventType.SubtractMoney)
    func = decorator(lambda: None)

    assert hasattr(func, "__event__")


@pytest.mark.asyncio
async def test_event_based_get_children() -> None:
    assert MockEventBased in EventBased.__subclasses__()
    assert len(MockEventBased.get_subscribers()) == 1
