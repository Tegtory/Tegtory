from tegtory.presenters.base_service import BaseService
from tegtory.presenters.bot import TegtorySingleton

from .handlers import router


class TegtoryService(BaseService):
    bot_singleton = TegtorySingleton

    def prepare_handlers(self) -> None:
        self.dp.include_routers(router)
