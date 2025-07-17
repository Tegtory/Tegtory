from typing import Any

from tegtory.common.exceptions import AppError

from ...results import Failure, Success
from ..base import DependencyRequired


class BaseCommandHandler[Command](DependencyRequired):
    object_type: Any

    async def __call__(self, command: Command) -> Success | Failure:
        try:
            return Success(data=await self.execute(command))
        except AppError as e:
            return Failure(reason=e.message)

    async def execute(self, command: Command) -> Any:
        raise NotImplementedError
