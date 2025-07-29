from typing import Protocol

from tegtory.domain.entities import User
from tegtory.domain.entities.user import RegisterUser, Wallet


class UserRepository(Protocol):
    async def get(self, item_id: int) -> User | None:
        pass

    async def create(self, user: RegisterUser) -> User:
        pass

    async def start_work(self, user_id: int, amount: float) -> None:
        pass


class WalletRepository(Protocol):
    async def get(self, tgid: int) -> Wallet | None:
        pass

    async def charge(self, tgid: int, amount: float) -> bool:
        pass

    async def add(self, tgid: int, amount: float) -> None:
        pass
