import dataclasses

from tegtory.domain.entities import StorageProduct
from tegtory.domain.entities.factory import StartFactoryEvent
from tegtory.domain.events import on_event
from tegtory.domain.events.event_types import EventType
from tegtory.domain.interfaces import EventBus, FactoryRepository
from tegtory.domain.services.work import WorkService
from tegtory.domain.use_cases.base import EventBased


@dataclasses.dataclass(frozen=True)
class FactoryEvent(EventBased):
    repository: FactoryRepository
    event_bus: EventBus

    @on_event(EventType.StartFactory)
    async def handle_start_factory(self, data: StartFactoryEvent) -> None:
        await WorkService.wait(data.time)

        bonus = data.factory.get_bonus(data)
        await self.repository.update(data.factory)
        await self.repository.add_product_in_storage(
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
