from tegtory.domain.entities import Factory, Product

from .base import BaseCommand


class FactoryRequiredCommand(BaseCommand):
    factory_id: int


class CreateFactoryCommand(BaseCommand):
    name: str
    id: int


class PayRequiredCommand(BaseCommand):
    user_id: int
    amount: float


class PayTaxCommand(BaseCommand):
    user_id: int


class UpgradeStorageCommand(BaseCommand):
    user_id: int


class UpgradeFactoryCommand(BaseCommand):
    user_id: int


class HireWorkerCommand(BaseCommand):
    user_id: int


class StartFactoryCommand(BaseCommand):
    factory: Factory
    time: float
    product: Product
