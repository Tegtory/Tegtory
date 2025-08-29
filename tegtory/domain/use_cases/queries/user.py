import dataclasses

from tegtory.domain.entities import User
from tegtory.domain.entities.user import Wallet
from tegtory.domain.interfaces import UserRepository
from tegtory.domain.interfaces.user import WalletRepository
from tegtory.domain.queries.user import UserQuery, WalletQuery
from tegtory.domain.use_cases.queries.base import BaseQueryHandler


@dataclasses.dataclass(frozen=True)
class GetUserQueryHandler(BaseQueryHandler[UserQuery]):
    repo: UserRepository

    async def handle(self, query: UserQuery) -> User | None:
        return await self.repo.get(query.user_id)


@dataclasses.dataclass(frozen=True)
class WalletQueryHandler(BaseQueryHandler[WalletQuery]):
    repo: WalletRepository

    async def handle(self, query: WalletQuery) -> Wallet | None:
        return await self.repo.get(query.user_id)
