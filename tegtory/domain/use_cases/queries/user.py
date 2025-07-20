import dataclasses

from tegtory.domain.entities import User
from tegtory.domain.interfaces import UserRepository
from tegtory.domain.queries.user import UserQuery
from tegtory.domain.use_cases.queries.base import BaseQueryHandler


@dataclasses.dataclass(frozen=True)
class GetUserQueryHandler(BaseQueryHandler):
    repo: UserRepository

    async def handle(self, query: UserQuery) -> User | None:
        return await self.repo.get(query.user_id)
