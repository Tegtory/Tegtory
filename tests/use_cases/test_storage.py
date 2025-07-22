from unittest.mock import AsyncMock, Mock

import pytest

from tegtory.domain.commands import UpgradeStorageCommand
from tegtory.domain.entities import Storage
from tegtory.domain.queries import GetStorageQuery
from tegtory.domain.results import Success
from tegtory.domain.use_cases.commands.storage import (
    UpgradeStorageCommandHandler,
)
from tegtory.domain.use_cases.queries.factory import GetStorageQueryHandler


@pytest.mark.asyncio
async def test_get_storage(storage_repository: Mock) -> None:
    handler = GetStorageQueryHandler(storage_repository)
    result = await handler(GetStorageQuery(factory_id=1))

    assert isinstance(result, Success)
    storage_repository.get.assert_called_with(1)


@pytest.mark.asyncio
async def test_upgrade_storage_success(storage_repository: Mock) -> None:
    money_mock = AsyncMock()
    money_mock.subtract = AsyncMock()
    handler = UpgradeStorageCommandHandler(
        storage_repo=storage_repository, money_repo=money_mock
    )
    result = await handler(
        UpgradeStorageCommand(
            storage=Storage(), user_id=1, user_money=1000, factory_id=1
        )
    )

    assert isinstance(result, Success)
    storage_repository.upgrade.assert_called_with(1)
