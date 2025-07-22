import contextlib
import os

from tegtory.infrastructure.events.events import subscribe_events
from tegtory.infrastructure.executor import preparing_executors
from tegtory.infrastructure.logger import configure_logger
from tegtory.presenters import TegtoryService


async def main() -> None:
    aiogram = asyncio.create_task(
        TegtoryService(os.environ.get("BOT_TOKEN"))()
    )
    await asyncio.gather(preparing_executors(), subscribe_events(), aiogram)


if __name__ == "__main__":
    import asyncio

    from dotenv import load_dotenv

    configure_logger()
    load_dotenv()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
