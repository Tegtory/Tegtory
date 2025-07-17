from tegtory.domain.entities import Storage
from tegtory.domain.interfaces.storage import StorageRepository


class StorageRepositoryImpl(StorageRepository):
    def __init__(self) -> None:
        self._storages: dict[int, Storage] = {}

    async def create(self, factory_id: int) -> Storage:
        self._storages[factory_id] = Storage()
        return self._storages[factory_id]

    async def upgrade(self, factory_id: int) -> None:
        self._storages[factory_id].upgrade()

    async def get(self, factory_id: int) -> Storage | None:
        return self._storages.get(factory_id)
