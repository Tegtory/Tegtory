import logging

from dishka import Provider, Scope, make_async_container, provide
from redis.asyncio import Redis

from tegtory.common.settings import settings
from tegtory.domain import services, use_cases
from tegtory.domain.interfaces import (
    EventBus,
    FactoryRepository,
    UserRepository,
)
from tegtory.domain.interfaces.storage import StorageRepository
from tegtory.domain.interfaces.user import WalletRepository
from tegtory.domain.use_cases.base import DependencyRequired

from .events.eventbus import MemoryEventBus
from .injectors import subscribe_all
from .repositories import FactoryRepositoryImpl
from .repositories.storage import StorageRepositoryImpl
from .repositories.user import RedisUserRepositoryImpl, WalletRepositoryImpl
from .utils import get_children, load_packages

logger = logging.getLogger(__name__)

load_packages(use_cases)
load_packages(services)

provider = Provider(scope=Scope.APP)

provider.provide(RedisUserRepositoryImpl, provides=UserRepository)
provider.provide(WalletRepositoryImpl, provides=WalletRepository)

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

    @provide(scope=Scope.APP)
    async def redis_connection(self) -> Redis:
        redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        return redis


container = make_async_container(provider, EventBusProvider())
