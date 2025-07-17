import dataclasses

from tegtory.domain.entities import Factory, Storage
from tegtory.domain.interfaces import FactoryRepository
from tegtory.domain.interfaces.storage import StorageRepository
from tegtory.domain.queries.factory import GetFactoryQuery, GetStorageQuery
from tegtory.domain.use_cases.queries.base import BaseQueryHandler


@dataclasses.dataclass(frozen=True)
class GetFactoryQueryHandler(BaseQueryHandler[GetFactoryQuery]):
    object_type = GetFactoryQuery

    repo: FactoryRepository

    async def handle(self, query: GetFactoryQuery) -> Factory | None:
        return await self.repo.get(query.factory_id)


@dataclasses.dataclass(frozen=True)
class GetStorageQueryHandler(BaseQueryHandler[GetStorageQuery]):
    object_type = GetStorageQuery

    repo: StorageRepository

    async def handle(self, query: GetStorageQuery) -> Storage | None:
        return await self.repo.get(query.factory_id)
