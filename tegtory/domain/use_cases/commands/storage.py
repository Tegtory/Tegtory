import dataclasses

from ...commands import UpgradeStorageCommand
from ...interfaces import UserRepository
from ...interfaces.storage import StorageRepository
from .base import BaseCommandHandler
from .pay_required import PayRequiredMixin, pay_required


@dataclasses.dataclass(frozen=True)
class UpgradeStorageCommandHandler(
    BaseCommandHandler[UpgradeStorageCommand], PayRequiredMixin
):
    storage_repo: StorageRepository
    money_repo: UserRepository

    @pay_required
    async def execute(self, cmd: UpgradeStorageCommand) -> None:
        await self.storage_repo.upgrade(cmd.factory_id)
