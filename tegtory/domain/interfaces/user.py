from tegtory.domain.entities import User
from tegtory.domain.interfaces.base import CrudRepository


class UserRepository(CrudRepository[User]):
    async def subtract(self, user_id: int, amount: float) -> None:
        pass

    async def add(self, user_id: int, amount: int) -> None:
        pass
