from ..entities import Factory, Product, StorageProduct
from ..entities.factory import StartFactoryEvent
from ..events import on_event
from ..events.event_types import EventType
from ..interfaces import EventBus, FactoryRepository
from ..services.factory import FactoryService
from ..services.money import MoneyService
from ..services.work import WorkService
from .base import EventBased, SafeCall


class UCFactory(SafeCall, EventBased):
    def __init__(
        self,
        repository: FactoryRepository,
        event_bus: EventBus,
        money: MoneyService,
        service: FactoryService,
    ):
        super().__init__(event_bus)
        self.repository = repository
        self.logic = service
        self.money = money

    async def find_product_by_name(
        self, factory: Factory, name: str
    ) -> Product | None:
        products = await self.repository.get_available_products(factory.id)
        return next((p for p in products if p.name == name), None)

    @on_event(EventType.StartFactory)
    async def handle_start_factory(self, data: StartFactoryEvent) -> None:
        await WorkService.wait(data.time)

        bonus = data.factory.get_bonus(data)
        await self.repository.update(data.factory)
        await self.insert_product_in_storage(
            StorageProduct(
                product=data.product,
                amount=bonus,
                storage=data.factory.storage,
            )
        )

        await self.event_bus.emit(
            EventType.EndFactoryWork,
            data={"factory": data.factory, "stock": bonus},
        )

    async def insert_product_in_storage(
        self, storage_product: StorageProduct
    ) -> None:
        await self.repository.add_product_in_storage(storage_product)
