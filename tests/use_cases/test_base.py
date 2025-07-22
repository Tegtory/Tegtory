from typing import Any

import pytest

from tegtory.common.exceptions import AppError
from tegtory.domain.results import Failure
from tegtory.domain.use_cases.queries.base import BaseQueryHandler


def raise_app_exception(self: type, cmd: Any) -> None:
    raise AppError


@pytest.mark.asyncio
async def test_base_query_handler_failure() -> None:
    handler: BaseQueryHandler = type(
        "Hander", (BaseQueryHandler,), {"handle": raise_app_exception}
    )()
    result = await handler(0)

    assert isinstance(result, Failure)
