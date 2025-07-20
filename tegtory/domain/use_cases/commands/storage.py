import dataclasses

from ...commands import UpgradeStorageCommand
from ...interfaces import UserRepository
from ...interfaces.storage import StorageRepository
from .base import BaseCommandHandler
from .pay_required import pay_required


@dataclasses.dataclass(frozen=True)
@pay_required
class UpgradeStorageCommandHandler(BaseCommandHandler[UpgradeStorageCommand]):
    storage_repo: StorageRepository
    money_repo: UserRepository

    async def execute(self, cmd: UpgradeStorageCommand) -> None:
        await self.storage_repo.upgrade(cmd.factory_id)
