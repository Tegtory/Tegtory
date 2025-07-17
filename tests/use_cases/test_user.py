import time
from unittest.mock import MagicMock

import pytest

from tegtory.domain.commands import RegisterUserCommand, StartUserWorkCommand
from tegtory.domain.entities import Factory, Product, User
from tegtory.domain.results import Failure, Success
from tegtory.domain.use_cases.commands.user import (
    RegisterUserCommandHandler,
    StartUserWorkCommandHandler,
)
from tegtory.domain.use_cases.event.user import UserEvent


@pytest.mark.asyncio
async def test_create_user(user_repo: MagicMock) -> None:
    expected_result = User(username="test", name="test", id=1)
    user_repo.create.return_value = expected_result

    query = RegisterUserCommandHandler(user_repo)
    result = await query(
        RegisterUserCommand(username="test", name="test", user_id=1)
    )

    assert isinstance(result, Success)
    assert isinstance(result.data, User)

    user_repo.create.assert_called_once_with(expected_result)


@pytest.mark.asyncio
async def test_subtract_money_failure_bad_data(user_repo: MagicMock) -> None:
    event = UserEvent(user_repo, MagicMock())
    result = await event._subtract_user_money({"user": 1, "amount": 30})

    assert not result
    user_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_start_user_work(
    user_repo: MagicMock, event_bus: MagicMock
) -> None:
    handler = StartUserWorkCommandHandler(user_repo, event_bus)

    cmd = StartUserWorkCommand(
        user=User(id=1, name="User", username="user", money=100),
        factory=Factory(id=1, name="Factory"),
        time=1,
        product=Product(name=""),
    )
    result = await handler(cmd)

    assert isinstance(result, Success)
    event_bus.emit.assert_called_once()
    user_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_start_user_work_failed_already_working(
    user_repo: MagicMock, event_bus: MagicMock
) -> None:
    handler = StartUserWorkCommandHandler(user_repo, event_bus)
    now = time.time()
    cmd = StartUserWorkCommand(
        user=User(
            id=1,
            name="User",
            username="user",
            money=100,
            end_work_time=now * 2,
        ),
        factory=Factory(id=1, name="Factory"),
        time=1,
        product=Product(name=""),
    )
    result = await handler(cmd)

    assert isinstance(result, Failure)
    event_bus.emit.assert_not_called()
    user_repo.update.assert_not_called()
