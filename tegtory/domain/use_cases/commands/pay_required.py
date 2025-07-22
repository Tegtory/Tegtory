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
        cmd.can_pay()
        result = await func(self, cmd)
        await self.money_repo.subtract(cmd.user_id, cmd.get_price())
        return result

    return wrapper
