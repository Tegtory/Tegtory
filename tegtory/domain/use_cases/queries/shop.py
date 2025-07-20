import dataclasses

from ...entities import Shop
from ...interfaces import ShopRepository
from ...queries.shop import (
    ListShopDeliveryQuery,
    ListShopNoDeliveryQuery,
    ListShopQuery,
    ShopQuery,
)
from .base import BaseQueryHandler


@dataclasses.dataclass(frozen=True)
class ListShopQueryHandler(BaseQueryHandler[ListShopQuery]):
    repo: ShopRepository

    async def handle(self, query: ListShopQuery) -> list[Shop]:
        return await self.repo.all()


@dataclasses.dataclass(frozen=True)
class ShopQueryHandler(BaseQueryHandler[ShopQuery]):
    repo: ShopRepository

    async def handle(self, query: ShopQuery) -> Shop | None:
        return await self.repo.by_name(query.title)


@dataclasses.dataclass(frozen=True)
class ListShopNoDeliveryQueryHandler(
    BaseQueryHandler[ListShopNoDeliveryQuery]
):
    repo: ShopRepository

    async def handle(self, query: ListShopNoDeliveryQuery) -> list[Shop]:
        return await self.repo.all_not_required_delivery()


@dataclasses.dataclass(frozen=True)
class ListShopDeliveryQueryHandler(BaseQueryHandler[ListShopDeliveryQuery]):
    repo: ShopRepository

    async def handle(self, query: ListShopDeliveryQuery) -> list[Shop]:
        return await self.repo.all_required_delivery()
