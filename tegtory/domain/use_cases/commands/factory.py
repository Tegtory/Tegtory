import dataclasses

from tegtory.common.exceptions import (
    AppError,
    FactoryRequiredError,
    NotEnoughPointsError,
)
from tegtory.domain.entities import Factory, Product
from tegtory.domain.interfaces.user import WalletRepository

from ...commands.factory import (
    CreateFactoryCommand,
    HireWorkerCommand,
    PayTaxCommand,
    StartFactoryCommand,
    UpgradeFactoryCommand,
)
from ...entities.factory import StartFactoryEvent
from ...events import EventType
from ...interfaces import EventBus, FactoryRepository
from ...interfaces.storage import StorageRepository
from ...services.factory import FactoryService
from .base import BaseCommandHandler

DEFAULT_AVAILABLE_PRODUCTS: list[Product] = [
    Product(
        name="Стулья",
        price_multiply=0.8,
        time_to_create=100,
        amount_multiply=0.8,
    ),
    Product(
        name="Кирпичи",
        price_multiply=0.9,
        time_to_create=160,
        amount_multiply=0.6,
    ),
    Product(
        name="Древесный Уголь",
        price_multiply=0.6,
        time_to_create=30,
        amount_multiply=1.2,
    ),
]


@dataclasses.dataclass(frozen=True, slots=True)
class CreateFactoryCommandHandler(BaseCommandHandler[CreateFactoryCommand]):
    repo: FactoryRepository
    storage: StorageRepository

    async def execute(self, cmd: CreateFactoryCommand) -> Factory:
        if await self.repo.by_name(cmd.name):
            raise AppError("Фабрика с таким именем уже существует")

        factory = await self.repo.create(Factory(name=cmd.name, id=cmd.id))
        factory.storage = await self.storage.create(factory.id)

        for product in DEFAULT_AVAILABLE_PRODUCTS:
            await self.repo.add_available_product(factory, product)
        return factory


@dataclasses.dataclass(frozen=True, slots=True)
class PayTaxCommandHandler(BaseCommandHandler[PayTaxCommand]):
    repo: FactoryRepository
    wallet: WalletRepository

    async def execute(self, cmd: PayTaxCommand) -> None:
        factory = await self.repo.get(cmd.user_id)
        if not factory:
            raise FactoryRequiredError
        if await self.wallet.charge(cmd.user_id, factory.tax):
            return await self.repo.set_tax(cmd.user_id, 0)
        raise NotEnoughPointsError


@dataclasses.dataclass(frozen=True, slots=True)
class UpgradeFactoryCommandHandler(BaseCommandHandler[UpgradeFactoryCommand]):
    repo: FactoryRepository
    wallet: WalletRepository

    async def execute(self, cmd: UpgradeFactoryCommand) -> None:
        factory = await self.repo.get(cmd.user_id)
        if not factory:
            raise FactoryRequiredError
        if await self.wallet.charge(cmd.user_id, factory.upgrade_price):
            return await self.repo.upgrade(factory.id)
        raise NotEnoughPointsError


@dataclasses.dataclass(frozen=True, slots=True)
class HireWorkerCommandHandler(BaseCommandHandler[HireWorkerCommand]):
    repo: FactoryRepository
    wallet: WalletRepository

    async def execute(self, cmd: HireWorkerCommand) -> None:
        factory = await self.repo.get(cmd.user_id)
        if not factory:
            raise FactoryRequiredError

        if await self.wallet.charge(cmd.user_id, factory.hire_price):
            factory.hire()
            return await self.repo.hire(factory.id)
        raise NotEnoughPointsError


@dataclasses.dataclass(frozen=True, slots=True)
class StartFactoryCommandHandler(BaseCommandHandler[StartFactoryCommand]):
    repository: FactoryRepository
    event_bus: EventBus
    logic: FactoryService

    async def execute(self, cmd: StartFactoryCommand) -> None:
        self.logic.start(cmd.factory, cmd.time)
        await self.repository.update(cmd.factory)

        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=cmd.factory,
                workers=cmd.factory.workers,
                time=cmd.time,
                product=cmd.product,
            ),
        )
