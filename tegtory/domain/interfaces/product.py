from typing import Protocol

from tegtory.domain.entities import Product


class ProductRepository(Protocol):
    async def by_name(self, name: str) -> Product | None:
        pass
