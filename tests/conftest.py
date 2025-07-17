from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from tegtory.domain.entities import Factory
from tegtory.domain.use_cases import UCFactory


@pytest.fixture
def mock_user() -> MagicMock:
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.money = 10000
    mock_user.name = "Test User"
    mock_user.username = "testuser"
    return mock_user


@pytest.fixture
def uc_factory(factory_repository: Mock) -> UCFactory:
    return UCFactory(factory_repository, AsyncMock(), AsyncMock(), AsyncMock())


@pytest.fixture
def factory_repository(mock_factory: Mock) -> Mock:
    mock = Mock()
    mock.get.return_value = None
    mock.by_name.return_value = None
    mock.create.return_value = mock_factory
    mock.upgrade.return_value = mock_factory
    return mock


@pytest.fixture
def mock_factory() -> Mock:
    mock = Mock(spec=Factory)
    mock.id = 1
    mock.name = "Test"
    mock.upgrade_price = 0
    mock.hire_price = 0
    mock.level = 12
    mock.workers = 0
    mock.tax = 10
    return mock


@pytest.fixture
def storage_repository(mock_factory: Mock) -> Mock:
    mock = Mock()
    mock.get = AsyncMock()
    mock.upgrade = AsyncMock()

    return mock


@pytest.fixture
def user_repo() -> MagicMock:
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.get = AsyncMock()
    return repo


@pytest.fixture
def shop_repo() -> MagicMock:
    repo = MagicMock()
    repo.by_name = AsyncMock()
    repo.all = AsyncMock()
    repo.all_required_delivery = AsyncMock()
    repo.all_not_required_delivery = AsyncMock()
    return repo


@pytest.fixture
def event_bus() -> MagicMock:
    bus = MagicMock()
    bus.emit = AsyncMock()
    return bus
