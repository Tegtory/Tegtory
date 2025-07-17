from ..shared.base_service import BaseService
from ..shared.bot import TegtorySingleton


class TegtoryService(BaseService):
    bot_singleton = TegtorySingleton

    def prepare_handlers(self) -> None:
        from ..shared.handlers.user import router as user_router
        from .handlers import router

        self.dp.include_routers(user_router, router)
