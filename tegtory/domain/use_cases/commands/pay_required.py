import dataclasses
from collections.abc import Callable
from functools import wraps
from typing import Any

from tegtory.domain.commands import PayRequiredCommand
from tegtory.domain.interfaces import UserRepository


@dataclasses.dataclass(frozen=True)
class PayRequiredMixin:
    money_repo: UserRepository


def pay_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self: PayRequiredMixin, cmd: PayRequiredCommand) -> Any:
        await self.money_repo.subtract(cmd.user_id, cmd.get_price())
        result = await func(self, cmd)
        return result

    return wrapper
