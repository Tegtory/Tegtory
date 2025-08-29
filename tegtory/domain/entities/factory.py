import dataclasses
import math
import time

from tegtory.common.deprecated import deprecated
from tegtory.common.exceptions import AppError, DuringWorkError
from tegtory.common.settings import HIRE_PRICE


@dataclasses.dataclass(frozen=True, kw_only=True)
class Product:
    name: str
    price_multiply: float = 1
    time_to_create: int = 10
    amount_multiply: float = 1

    def __hash__(self) -> int:
        return hash(self.name)


@dataclasses.dataclass()
class Storage:
    max_stock: int = 20
    products: dict[Product, int] = dataclasses.field(default_factory=dict)

    @property
    def stock(self) -> int:
        return sum(self.products.values())

    @property
    def upgrade_price(self) -> int:
        return self.max_stock // 2 + 78

    def upgrade(self) -> None:
        self.max_stock += 10

    def is_can_insert(self, product_amount: int) -> bool:
        return (self.stock + product_amount) <= self.max_stock

    def get_available_amount(self) -> int:
        return self.max_stock - self.stock

    def adjust_bonus(self, bonus: int) -> int:
        if not self.is_can_insert(bonus):
            bonus = self.get_available_amount()
        return bonus


@dataclasses.dataclass(frozen=True, kw_only=True)
class StorageProduct:
    product: Product
    storage: Storage
    amount: int


@dataclasses.dataclass(frozen=True, kw_only=True)
class AvailableProduct:
    product: Product
    factory: "Factory"


@dataclasses.dataclass(frozen=True, kw_only=True)
class StartFactoryEvent:
    factory: "Factory"
    time: float | int
    product: Product
    workers: int = 1


@dataclasses.dataclass(kw_only=True)
class Factory:
    id: int
    name: str
    storage: Storage = dataclasses.field(default_factory=lambda: Storage())
    money_invested: int = 0
    end_work_time: float = 0.0
    tax: int = 1
    workers: int = 0

    def __str__(self) -> str:
        return f"""\
🏭 *{self.name}*
🔧 *Вложения:* {self.money_invested}
🚧 *Статус:* {"Работает" if self.state else "Не работает"}
💸 *Налоги:* {self.tax}
👷‍ *Работники:* {self.workers}
"""

    @property
    def minutes_to_work(self) -> float:
        return math.ceil(self.work_time_remained / 60 * 10) / 10

    @property
    def hire_price(self) -> int:
        return max(1, self.workers) * HIRE_PRICE

    @property
    @deprecated
    def hire_available(self) -> int:
        return True

    @property
    @deprecated
    def upgrade_price(self) -> int:
        return math.ceil(370 * (1.05 ** (5 - 1)) * (5 // 2) ** 1.2)

    @property
    def work_time_remained(self) -> float:
        return self.end_work_time - time.time()

    @property
    def state(self) -> bool:
        return self.work_time_remained > 0.0

    def start_work(self, time_amount: float) -> float:
        if not self.state:
            self.end_work_time = time.time() + time_amount
        return self.end_work_time

    def rename(self, name: str) -> None:
        self.name = name

    def hire(self) -> None:
        if self.state:
            raise DuringWorkError
        if self.hire_available <= 0:
            raise AppError("Вы достигли лимита рабочих для данного уровня")
        self.workers += 1

    def set_tax(self, amount: int) -> None:
        self.tax = 4 * amount // 3

    def get_bonus(self, data: StartFactoryEvent) -> int:
        bonus = self.calculate_bonus(data)
        bonus = self.storage.adjust_bonus(bonus)
        self.set_tax(bonus)
        return bonus

    @staticmethod
    def calculate_bonus(data: StartFactoryEvent) -> int:
        return int(data.time // data.product.time_to_create) * data.workers
