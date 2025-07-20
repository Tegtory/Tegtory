from aiogram import Router

from .city import router as city
from .factory import router as factory
from .start import router as start
from .user import router as user

router = Router()
router.include_routers(city, factory, start, user)

__all__ = ["router"]
