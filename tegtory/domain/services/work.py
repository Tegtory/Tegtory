import asyncio

from tegtory.domain.use_cases.base import DependencyRequired


class WorkService(DependencyRequired):
    @staticmethod
    async def wait(time: float) -> None:
        await asyncio.sleep(time)
