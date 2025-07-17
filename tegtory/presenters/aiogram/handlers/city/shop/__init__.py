from aiogram import Router

from .main import router as main

router = Router()


router.include_routers(main)

__all__ = ["router"]
