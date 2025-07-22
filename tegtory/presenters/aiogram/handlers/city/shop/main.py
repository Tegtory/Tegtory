from typing import TYPE_CHECKING, Any

from aiogram import F, Router, types

from tegtory.domain.queries import (
    ListShopDeliveryQuery,
    ListShopNoDeliveryQuery,
    ListShopQuery,
    ShopQuery,
)
from tegtory.domain.queries.base import BaseQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure import QueryExecutor
from tegtory.presenters.aiogram.kb import CityCB
from tegtory.presenters.aiogram.kb import shop as kb
from tegtory.presenters.aiogram.messages import shop as msg

if TYPE_CHECKING:
    from tegtory.domain.entities import Shop

router = Router()


@router.callback_query(F.data.startswith(f"{CityCB.shop}-"))
@router.callback_query(F.data == CityCB.shop)
async def shop_list(
    call: types.CallbackQuery, query_executor: QueryExecutor
) -> Any:
    query_type = get_shop_list_query_type(call.data) or ListShopQuery

    shops: Success[list[Shop]] | Failure = await query_executor.ask(
        query_type()
    )
    if isinstance(shops, Success):
        markup = kb.get_shop_list_markup(shops.data)
        await call.message.edit_caption(
            caption=msg.shop_list, reply_markup=markup
        )


@router.callback_query(F.data.startswith(f"{CityCB.shop}:"))
async def shop_page(
    call: types.CallbackQuery, query_executor: QueryExecutor
) -> None:
    shop_data = await query_executor.ask(
        ShopQuery(title=call.data.split(":")[1])
    )
    if isinstance(shop_data, Success):
        shop: Shop = shop_data.data
        markup = kb.get_shop_markup(shop)
        await call.message.edit_caption(
            caption=msg.specific_shop.format(
                shop.title, shop.description, shop.delivery_required
            ),
            reply_markup=markup,
        )


def get_shop_list_query_type(data: str | None) -> type[BaseQuery] | None:
    if not data:
        data = "s-"

    for i in filter(
        lambda x: x.__name__ == data.split("-")[-1],
        {ListShopNoDeliveryQuery, ListShopDeliveryQuery},
    ):
        return i
    return None
