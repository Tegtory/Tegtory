from typing import Protocol

from tegtory.domain.entities import Shop, ShopProduct
from tegtory.domain.interfaces.base import CrudRepository


class ShopRepository(CrudRepository[Shop], Protocol):
    async def all_required_delivery(self) -> list[Shop]:
        pass

    async def all_not_required_delivery(self) -> list[Shop]:
        pass

    async def by_name(self, name: str) -> Shop | None:
        pass

    async def add_product(self, product: ShopProduct) -> ShopProduct:
        pass

    async def get_products(self, shop: Shop) -> list[ShopProduct]:
        pass

    async def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        pass
