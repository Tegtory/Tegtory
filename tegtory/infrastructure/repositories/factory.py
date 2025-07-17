import logging
from typing import ClassVar

from tegtory.domain.entities import Factory, Product, StorageProduct
from tegtory.domain.interfaces import FactoryRepository

logger = logging.getLogger(__name__)


class FactoryRepositoryImpl(FactoryRepository):
    _factories: ClassVar[list[Factory]] = []

    def __init__(self) -> None:
        self.available_products: dict[int, list[Product]] = {}

    @classmethod
    def _filter_factories(cls, user_id: int) -> Factory | None:
        for i in filter(lambda u: u.id == user_id, cls._factories):
            return i
        return None

    async def get(self, owner_id: int) -> Factory | None:
        return self._filter_factories(owner_id)

    async def by_name(self, name: str) -> Factory | None:
        for i in filter(lambda f: f.name == name, self._factories):
            return i
        return None

    async def create(self, factory: Factory) -> Factory:
        logger.info(f"Creating Factory {factory.name} by user {factory.id}")
        self._factories.append(factory)
        return factory

    async def upgrade(self, factory_id: int) -> None:
        factory = self._filter_factories(factory_id)
        if factory:
            factory.level += 1

    async def update(self, factory: Factory) -> Factory:
        return factory

    async def add_available_product(
        self, factory: Factory, product: Product
    ) -> tuple[Factory, Product]:
        if not self.available_products.get(factory.id):
            self.available_products[factory.id] = []
        self.available_products[factory.id].append(product)
        return factory, product

    async def get_available_products(self, factory: Factory) -> list[Product]:
        return self.available_products.get(factory.id, [])

    async def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        storage = storage_product.storage
        if not storage.products.get(storage_product.product):
            storage.products[storage_product.product] = 0
        storage.products[storage_product.product] += storage_product.amount

        return storage_product

    async def set_tax(self, factory_id: int, amount: int) -> None:
        factory = self._filter_factories(factory_id)
        if factory:
            factory.tax = amount

    async def hire(self, factory_id: int) -> None:
        """
        While system in-memory
        we don't need change here all proceeded in factory.hire()
        """
        pass
