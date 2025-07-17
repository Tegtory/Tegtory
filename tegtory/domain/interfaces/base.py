from typing import Protocol


class CrudRepository[T](Protocol):
    async def all(self) -> list[T]:
        pass

    async def get(self, item_id: int) -> T | None:
        pass

    async def create(self, item: T) -> T:
        pass

    async def update(self, item: T) -> T:
        pass

    async def delete(self, item_id: int) -> None:
        pass
