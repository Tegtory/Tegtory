from tegtory.domain.entities import Shop, ShopProduct
from tegtory.domain.interfaces import ShopRepository


class ShopRepositoryImpl(ShopRepository):
    def __init__(self) -> None:
        self.shops: list[Shop] = [
            Shop(id=1, title="dd", description="dsd", distance=1),
            Shop(id=2, title="second", description="dsd", distance=10),
        ]
        self.shop_products: list[ShopProduct] = []

    async def all(self) -> list[Shop]:
        return self.shops

    async def get(self, item_id: int) -> Shop | None:
        for i in filter(lambda shop: shop.id == item_id, self.shops):
            return i
        return None

    async def all_required_delivery(self) -> list[Shop]:
        return [i for i in filter(lambda x: x.delivery_required, self.shops)]

    async def all_not_required_delivery(self) -> list[Shop]:
        return [
            i for i in filter(lambda x: not x.delivery_required, self.shops)
        ]

    async def create(self, item: Shop) -> Shop:
        self.shops.append(item)
        item.id = len(self.shops)
        return item

    async def update(self, item: Shop) -> Shop:
        return item

    async def by_name(self, name: str) -> Shop | None:
        for i in filter(lambda shop: shop.title == name, self.shops):
            return i
        return None
