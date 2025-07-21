import logging

from tegtory.domain.commands.base import BaseCommand
from tegtory.domain.results import Failure, Success
from tegtory.domain.use_cases.commands.base import BaseCommandHandler
from tegtory.infrastructure.executor import BaseExecutor

logger = logging.getLogger(__name__)


class CommandExecutor(BaseExecutor):
    handler_base_class = BaseCommandHandler

    async def execute(self, command: BaseCommand) -> Success | Failure:
        logger.info(
            f"Executing command: {command.__class__.__name__}({command})"
        )
        return await self.handlers[type(command)](command)
