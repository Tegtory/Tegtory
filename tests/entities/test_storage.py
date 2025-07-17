import pytest

from tegtory.domain.entities import Product, Storage


@pytest.mark.asyncio
async def test_storage_stock_calculation() -> None:
    stor = Storage()
    stock = 31
    stor.products = {Product(name=""): stock}

    assert stor.stock == stock


@pytest.mark.asyncio
async def test_storage_upgrade() -> None:
    stor = Storage()
    stor.upgrade()

    assert stor.max_stock == Storage().max_stock + 10


@pytest.mark.asyncio
async def test_storage_can_insert() -> None:
    stor = Storage()
    stor.products = {Product(name=""): 31}
    assert not stor.is_can_insert(1)


@pytest.mark.asyncio
async def test_get_available_amount() -> None:
    stor = Storage()
    stor.products = {Product(name=""): stor.max_stock}
    assert stor.get_available_amount() == 0


@pytest.mark.asyncio
async def test_adjust_bonus_return_zero() -> None:
    stor = Storage()
    assert stor.adjust_bonus(0) == 0


@pytest.mark.asyncio
async def test_adjust_bonus_return_maximum_value() -> None:
    stor = Storage()
    assert stor.adjust_bonus(stor.max_stock + 1) == stor.max_stock
