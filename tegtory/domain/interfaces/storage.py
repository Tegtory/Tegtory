from typing import Protocol

from tegtory.domain.entities import Storage


class StorageRepository(Protocol):
    async def get(self, factory_id: int) -> Storage | None:
        pass

    async def upgrade(self, factory_id: int) -> None:
        pass

    async def create(self, factory_id: int) -> Storage:
        pass

    async def insert_product_in_storage(
        self, factory_id: int, product_id: int, amount: int
    ) -> None:
        pass
