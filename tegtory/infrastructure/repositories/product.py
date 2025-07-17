from tegtory.domain.entities import Product
from tegtory.domain.interfaces.product import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self) -> None:
        self.products: list[Product] = []

    async def by_name(self, name: str) -> Product | None:
        for i in filter(lambda p: p.name == name, self.products):
            return i
        return None

    async def all(self) -> list[Product]:
        return self.products

    async def create(self, product: Product) -> Product:
        self.products.append(product)
        return product

    async def update(self, product: Product) -> Product:
        return product
