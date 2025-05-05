import logging

from domain.commands.base import BaseCommand
from domain.results import Failure, Success
from domain.use_cases.commands.base import BaseCommandHandler
from infrastructure.executor import BaseExecutor

logger = logging.getLogger(__name__)


class CommandExecutor(BaseExecutor):
    handler_base_class: type[BaseCommandHandler] = BaseCommandHandler

    async def execute(self, command: BaseCommand) -> Success | Failure:
        logger.info(f"Executing command: {command.__class__.__name__}({command})")
        return await self.handlers[type(command)](command)
