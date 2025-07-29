from .city import router as city
from .errors import router
from .factory import router as factory
from .start import router as start
from .user import router as user

router.include_routers(city, factory, start, user)

__all__ = ["router"]
