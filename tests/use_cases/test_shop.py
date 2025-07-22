from unittest.mock import Mock

import pytest

from tegtory.domain.queries import (
    ListShopDeliveryQuery,
    ListShopNoDeliveryQuery,
    ListShopQuery,
    ShopQuery,
)
from tegtory.domain.results import Success
from tegtory.domain.use_cases.queries.shop import (
    ListShopDeliveryQueryHandler,
    ListShopNoDeliveryQueryHandler,
    ListShopQueryHandler,
    ShopQueryHandler,
)


@pytest.mark.asyncio
async def test_shop_query(shop_repo: Mock) -> None:
    handler = ShopQueryHandler(shop_repo)
    result = await handler(ShopQuery(title=""))

    assert isinstance(result, Success)
    shop_repo.by_name.assert_called_once()


@pytest.mark.asyncio
async def test_list_shop_no_delivery(shop_repo: Mock) -> None:
    handler = ListShopNoDeliveryQueryHandler(shop_repo)
    result = await handler(ListShopNoDeliveryQuery())

    assert isinstance(result, Success)
    shop_repo.all_not_required_delivery.assert_called_once()


@pytest.mark.asyncio
async def test_list_shop(shop_repo: Mock) -> None:
    handler = ListShopQueryHandler(shop_repo)
    result = await handler(ListShopQuery())

    assert isinstance(result, Success)
    shop_repo.all.assert_called_once()


@pytest.mark.asyncio
async def test_list_shop_with_delivery(shop_repo: Mock) -> None:
    handler = ListShopDeliveryQueryHandler(shop_repo)
    result = await handler(ListShopDeliveryQuery())

    assert isinstance(result, Success)
    shop_repo.all_required_delivery.assert_called_once()
