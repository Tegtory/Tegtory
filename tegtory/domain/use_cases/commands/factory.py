import dataclasses

from tegtory.common.exceptions import AppError
from tegtory.domain.entities import Factory, Product

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
from .pay_required import PayRequiredMixin, pay_required

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


@dataclasses.dataclass(frozen=True)
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


@dataclasses.dataclass(frozen=True)
class PayTaxCommandHandler(
    BaseCommandHandler[PayTaxCommand], PayRequiredMixin
):
    repo: FactoryRepository

    @pay_required
    async def execute(self, cmd: PayTaxCommand) -> None:
        await self.repo.set_tax(cmd.factory_id, 0)


@dataclasses.dataclass(frozen=True)
class UpgradeFactoryCommandHandler(
    BaseCommandHandler[UpgradeFactoryCommand], PayRequiredMixin
):
    repo: FactoryRepository

    @pay_required
    async def execute(self, cmd: UpgradeFactoryCommand) -> None:
        await self.repo.upgrade(cmd.factory_id)


@dataclasses.dataclass(frozen=True)
class HireWorkerCommandHandler(
    BaseCommandHandler[HireWorkerCommand], PayRequiredMixin
):
    repo: FactoryRepository

    @pay_required
    async def execute(self, cmd: HireWorkerCommand) -> None:
        cmd.factory.hire()
        await self.repo.hire(cmd.factory.id)


@dataclasses.dataclass(frozen=True)
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
