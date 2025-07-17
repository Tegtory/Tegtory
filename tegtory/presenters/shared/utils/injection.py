import inspect
from collections.abc import Callable
from typing import Any


async def smart_call(
    func: Callable, *args: tuple, **kwargs: dict[str, Any]
) -> Any:
    sig = inspect.signature(func)
    arg_names = set(sig.parameters)
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in arg_names}
    return await func(*args, **filtered_kwargs)
