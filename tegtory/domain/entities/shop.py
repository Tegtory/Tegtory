import dataclasses
from datetime import datetime

from tegtory.common.settings import DELIVERY_MIN_DISTANT
from tegtory.domain.entities.contract import BaseContract
from tegtory.domain.entities.factory import Factory, Product


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


@dataclasses.dataclass(kw_only=True, frozen=True)
class ShopContract(BaseContract):
    shop: Shop
    factory: Factory
    product: Product
    amount: int
    price_per_one: int
    delivery_required: bool = False
