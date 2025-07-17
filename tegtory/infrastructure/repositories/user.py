import logging
from typing import ClassVar

from tegtory.domain.entities import User
from tegtory.domain.interfaces import UserRepository

logger = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    _users: ClassVar[list[User]] = []

    def _filter_users(self, user_id: int) -> User | None:
        for i in filter(lambda u: u.id == user_id, self._users):
            return i
        return None

    async def get(self, user_id: int) -> User | None:
        return self._filter_users(user_id)

    async def create(self, user: User) -> User:
        logger.info(f"Creating user {user.id} with name {user.name}")
        self._users.append(user)
        return user

    async def update(self, user: User) -> User:
        return user

    async def send(
        self, from_user_id: int, to_user_id: int, amount: int
    ) -> None:
        pass

    async def subtract(self, user_id: int, amount: int) -> None:
        user = self._filter_users(user_id)
        if user:
            logger.info(f"Subtracting user {user_id} with amount {amount}")
            user.money -= amount

    async def add(self, user_id: int, amount: int) -> None:
        user = self._filter_users(user_id)
        if user:
            user.money += amount
