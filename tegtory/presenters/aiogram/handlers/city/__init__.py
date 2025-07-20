from aiogram import Router

from .main import router as main
from .sell_product import router as sell_product
from .shop import router as shop

router = Router()
router.include_routers(main, shop, sell_product)

__all__ = ["router"]
