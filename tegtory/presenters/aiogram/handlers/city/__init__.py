from aiogram import Router

from .main import router as main
from .sell_product import router as sell_product

router = Router()

router.include_routers(main, sell_product)

__all__ = ["router"]
