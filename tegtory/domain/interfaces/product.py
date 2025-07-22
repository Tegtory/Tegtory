from tegtory.domain.entities import Product
from tegtory.domain.interfaces.base import CrudRepository


class ProductRepository(CrudRepository[Product]):
    async def by_name(self, name: str) -> Product | None:
        pass
