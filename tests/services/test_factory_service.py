import math
from unittest.mock import Mock

import pytest

from tegtory.common.exceptions import AppError, TaxError
from tegtory.domain.services.factory import FactoryService


@pytest.mark.asyncio
async def test_hire_worker_successfully(mock_factory: Mock) -> None:
    mock_factory.hire_available = 1
    result = FactoryService.hire_worker(mock_factory)

    mock_factory.hire.assert_called_once()
    assert result == mock_factory


@pytest.mark.asyncio
async def test_hire_worker_failure_working_max_workers(
    mock_factory: Mock,
) -> None:
    mock_factory.hire_available = 0

    with pytest.raises(AppError):
        FactoryService.hire_worker(mock_factory)

    mock_factory.hire.assert_not_called()


@pytest.mark.asyncio
async def test_factory_start_success(mock_factory: Mock) -> None:
    mock_factory.state = False
    mock_factory.workers = 1
    mock_factory.tax = 0

    FactoryService.start(mock_factory, 1)

    mock_factory.start_work.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_factory_start_failure_workers_zero(mock_factory: Mock) -> None:
    mock_factory.state = False
    mock_factory.workers = 0
    mock_factory.tax = 0

    with pytest.raises(AppError):
        FactoryService.start(mock_factory, 1)

    mock_factory.start_work.assert_not_called()


@pytest.mark.asyncio
async def test_factory_start_failure_already_working(
    mock_factory: Mock,
) -> None:
    mock_factory.state = False
    mock_factory.workers = 1
    mock_factory.tax = math.inf

    with pytest.raises(TaxError):
        FactoryService.start(mock_factory, 1)

    mock_factory.start_work.assert_not_called()


@pytest.mark.asyncio
async def test_factory_start_failure_tax_limit(mock_factory: Mock) -> None:
    mock_factory.state = True

    result = FactoryService.start(mock_factory, 1)

    mock_factory.start_work.assert_not_called()
    assert not result
