import logging

from dishka import Provider, Scope, make_async_container, provide

from tegtory.domain import services, use_cases
from tegtory.domain.interfaces import (
    EventBus,
    FactoryRepository,
    ShopRepository,
    UserRepository,
)
from tegtory.domain.interfaces.storage import StorageRepository
from tegtory.domain.use_cases.base import DependencyRequired

from .events.eventbus import MemoryEventBus
from .injectors import subscribe_all
from .repositories import (
    FactoryRepositoryImpl,
    ShopRepositoryImpl,
    UserRepositoryImpl,
)
from .repositories.storage import StorageRepositoryImpl
from .utils import get_children, load_packages

logger = logging.getLogger(__name__)

load_packages(use_cases)
load_packages(services)

provider = Provider(scope=Scope.APP)
provider.provide(UserRepositoryImpl, provides=UserRepository)

provider.provide(ShopRepositoryImpl, provides=ShopRepository)

provider.provide(FactoryRepositoryImpl, provides=FactoryRepository)
provider.provide(StorageRepositoryImpl, provides=StorageRepository)

for child in get_children(DependencyRequired):
    provider.provide(child)


class EventBusProvider(Provider):
    @provide(scope=Scope.APP)
    async def new_connection(self) -> EventBus:
        logger.info("Preparing EventBus")
        event_bus = MemoryEventBus()

        subscribe_all(event_bus)
        logger.info("Successfully prepared")
        return event_bus


container = make_async_container(provider, EventBusProvider())
