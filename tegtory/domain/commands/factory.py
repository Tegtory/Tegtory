from tegtory.common.exceptions import NotEnoughPointsError
from tegtory.domain.entities import Factory, Product, Storage

from .base import BaseCommand


class FactoryRequiredCommand(BaseCommand):
    factory_id: int


class CreateFactoryCommand(BaseCommand):
    name: str
    id: int


class PayRequiredCommand(BaseCommand):
    user_id: int
    user_money: int

    def can_pay(self) -> None:
        if self.user_money < self.get_price():
            raise NotEnoughPointsError()

    def get_price(self) -> float | int:
        raise NotImplementedError


class PayTaxCommand(PayRequiredCommand, FactoryRequiredCommand):
    factory_tax: int

    def get_price(self) -> float | int:
        return self.factory_tax


class UpgradeStorageCommand(PayRequiredCommand, FactoryRequiredCommand):
    storage: Storage

    def get_price(self) -> float | int:
        return self.storage.upgrade_price


class UpgradeFactoryCommand(PayRequiredCommand, FactoryRequiredCommand):
    factory_upgrade_price: int

    def get_price(self) -> float | int:
        return self.factory_upgrade_price


class HireWorkerCommand(PayRequiredCommand):
    factory: Factory

    def get_price(self) -> float | int:
        return self.factory.hire_price


class StartFactoryCommand(BaseCommand):
    factory: Factory
    time: float
    product: Product
