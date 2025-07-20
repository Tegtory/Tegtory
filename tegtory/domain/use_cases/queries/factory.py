import dataclasses

from tegtory.domain.entities import Factory, Product, Storage
from tegtory.domain.interfaces import FactoryRepository
from tegtory.domain.interfaces.storage import StorageRepository
from tegtory.domain.queries.factory import (
    GetAvailableProductsQuery,
    GetFactoryQuery,
    GetStorageQuery,
)
from tegtory.domain.use_cases.queries.base import BaseQueryHandler


@dataclasses.dataclass(frozen=True)
class GetFactoryQueryHandler(BaseQueryHandler[GetFactoryQuery]):
    repo: FactoryRepository

    async def handle(self, query: GetFactoryQuery) -> Factory | None:
        return await self.repo.get(query.factory_id)


@dataclasses.dataclass(frozen=True)
class GetStorageQueryHandler(BaseQueryHandler[GetStorageQuery]):
    repo: StorageRepository

    async def handle(self, query: GetStorageQuery) -> Storage | None:
        return await self.repo.get(query.factory_id)


@dataclasses.dataclass(frozen=True)
class GetAvailableProductsQueryHandler(
    BaseQueryHandler[GetAvailableProductsQuery]
):
    repo: FactoryRepository

    async def handle(self, query: GetAvailableProductsQuery) -> list[Product]:
        return await self.repo.get_available_products(query.factory_id)
