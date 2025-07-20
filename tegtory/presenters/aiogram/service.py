from tegtory.presenters.base_service import BaseService
from tegtory.presenters.bot import TegtorySingleton


class TegtoryService(BaseService):
    bot_singleton = TegtorySingleton

    def prepare_handlers(self) -> None:
        from .handlers import router

        self.dp.include_routers(router)
