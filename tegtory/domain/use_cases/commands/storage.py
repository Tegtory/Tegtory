import dataclasses

from tegtory.common.exceptions import (
    FactoryRequiredError,
    NotEnoughPointsError,
)
from tegtory.domain.interfaces.user import WalletRepository

from ...commands import UpgradeStorageCommand
from ...interfaces.storage import StorageRepository
from .base import BaseCommandHandler


@dataclasses.dataclass(frozen=True)
class UpgradeStorageCommandHandler(BaseCommandHandler[UpgradeStorageCommand]):
    storage_repo: StorageRepository
    money_repo: WalletRepository

    async def execute(self, cmd: UpgradeStorageCommand) -> None:
        storage = await self.storage_repo.get(cmd.user_id)
        if not storage:
            raise FactoryRequiredError
        if self.money_repo.charge(cmd.user_id, storage.upgrade_price):
            return await self.storage_repo.upgrade(cmd.user_id)
        raise NotEnoughPointsError
