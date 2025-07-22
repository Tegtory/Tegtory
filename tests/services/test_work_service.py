import pytest

from tegtory.domain.services import work


@pytest.mark.asyncio
@pytest.mark.timeout(1.1)
async def test_work_service() -> None:
    await work.WorkService.wait(1)
