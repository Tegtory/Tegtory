from typing import Any

from tegtory.common.exceptions import AppError
from tegtory.domain.results import Failure, Success

from ..base import DependencyRequired


class BaseQueryHandler[Query](DependencyRequired):
    async def __call__(self, query: Query) -> Success | Failure:
        try:
            return Success(data=await self.handle(query))
        except AppError as e:
            return Failure(reason=e.message)

    async def handle(self, query: Query) -> Any:
        raise NotImplementedError
