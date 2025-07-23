from typing import Protocol

from tegtory.domain.entities import User
from tegtory.domain.entities.user import RegisterUser


class UserRepository(Protocol):
    async def get(self, item_id: int) -> User | None:
        pass

    async def create(self, item: RegisterUser) -> User:
        pass

    async def subtract(self, user_id: int, amount: float) -> None:
        pass

    async def add(self, user_id: int, amount: int) -> None:
        pass

    async def start_work(self, user_id: int, amount: float) -> None:
        pass
