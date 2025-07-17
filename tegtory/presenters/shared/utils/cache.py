import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from tegtory.presenters.shared.utils.injection import smart_call

logger = logging.getLogger("cache")
_temp: dict = {}


def cache(item: Any, default: Any) -> Callable:
    def cache_func(x: Any) -> None:
        if x not in _temp.values():
            logger.debug(f"Caching {str(item)[:50]} with value {str(x)[:25]}")
            _temp.update({item: x})

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any:
            return await smart_call(
                func,
                *args,
                **{
                    "cached": _temp.get(item, default),
                    "cache_func": cache_func,
                    **kwargs,
                },
            )

        return wrapper

    return decorator
