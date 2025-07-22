from unittest.mock import Mock

import pytest

from tegtory.common.exceptions import AppError
from tegtory.domain.events import EventType
from tegtory.domain.services.money import MoneyService


@pytest.mark.asyncio
async def test_money_service_success(event_bus: Mock, mock_user: Mock) -> None:
    service = MoneyService(event_bus)
    mock_user.can_buy.return_value = True

    await service.charge(mock_user, 1)

    event_bus.emit.assert_called_with(
        EventType.SubtractMoney, data={"user": mock_user, "amount": 1}
    )


@pytest.mark.asyncio
async def test_money_service_failure_cannot_buy(
    event_bus: Mock, mock_user: Mock
) -> None:
    service = MoneyService(event_bus)
    mock_user.can_buy.return_value = False

    with pytest.raises(AppError):
        await service.charge(mock_user, 1)
    event_bus.emit.assert_not_called()
