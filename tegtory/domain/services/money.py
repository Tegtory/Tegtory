from tegtory.common.exceptions import NotEnoughPointsError
from tegtory.domain.entities import User
from tegtory.domain.events import EventType
from tegtory.domain.use_cases.base import EventBased


class MoneyService(EventBased):
    async def charge(self, user: User, amount: int) -> None:
        if not user.can_buy(amount):
            raise NotEnoughPointsError
        await self.event_bus.emit(
            EventType.SubtractMoney, data={"user": user, "amount": amount}
        )
