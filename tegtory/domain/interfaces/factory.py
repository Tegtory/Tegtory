from typing import Protocol

from tegtory.domain.entities import Factory, Product, StorageProduct
from tegtory.domain.interfaces.base import CrudRepository


class FactoryRepository(CrudRepository[Factory], Protocol):
    async def by_name(self, name: str) -> Factory | None:
        pass

    async def add_available_product(
        self, factory: Factory, product: Product
    ) -> tuple[Factory, Product]:
        pass

    async def get_available_products(self, factory: Factory) -> list[Product]:
        pass

    async def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        pass

    async def hire(self, factory_id: int) -> None:
        pass

    async def upgrade(self, factory_id: int) -> None:
        pass

    async def set_tax(self, factory_id: int, value: int) -> None:
        pass
