from aiogram import Router

from .main import router as main
from .shop import router as shop

router = Router()
router.include_routers(main, shop)

__all__ = ["router"]
