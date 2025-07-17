from aiogram import Router

from .crud import router as create
from .hire import router as hire
from .main import router as main
from .start import router as start
from .storage import router as storage
from .tax import router as tax

router = Router()
router.include_routers(main, create, start, hire, tax, storage)

__all__ = ["router"]
