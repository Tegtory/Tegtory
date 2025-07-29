from typing import Any

from tegtory.common.exceptions import (
    AppError,
    DuringWorkError,
    FactoryRequiredError,
    NotEnoughPointsError,
)

from ...results import Failure, Success
from ..base import DependencyRequired

EXCLUDED_ERRORS = [NotEnoughPointsError, DuringWorkError, FactoryRequiredError]


class BaseCommandHandler[Command](DependencyRequired):
    async def __call__(self, cmd: Command) -> Success | Failure:
        try:
            return Success(data=await self.execute(cmd))
        except AppError as e:
            if type(e) in EXCLUDED_ERRORS:
                raise e from e
            return Failure(reason=e.message)

    async def execute(self, command: Command) -> Any:
        raise NotImplementedError
