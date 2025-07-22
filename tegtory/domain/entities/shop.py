import dataclasses
from datetime import datetime

from tegtory.common.settings import DELIVERY_MIN_DISTANT
from tegtory.domain.entities.factory import Product


@dataclasses.dataclass(kw_only=True)
class Shop:
    id: int
    title: str
    description: str
    distance: int
    is_bot: bool = True

    @property
    def delivery_required(self) -> bool:
        return self.distance >= DELIVERY_MIN_DISTANT


@dataclasses.dataclass(kw_only=True)
class ShopProduct:
    id: int = 0
    shop: Shop
    product: Product
    amount: int
    is_demand: bool = False
    created_at: datetime = dataclasses.field(default_factory=datetime.now)
