from aiogram import F, Router, types

from tegtory.domain.entities import Factory, Product
from tegtory.domain.queries.factory import GetAvailableProductsQuery
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure import QueryExecutor
from tegtory.presenters.aiogram.kb import city as kb
from tegtory.presenters.aiogram.kb.callbacks import CityCB, SellProductCallback
from tegtory.presenters.aiogram.messages import city as msg
from tegtory.presenters.aiogram.utils import get_factory

router = Router()


@router.callback_query(F.data == CityCB.sell_product)
@get_factory
async def sell_product(
    call: types.CallbackQuery, factory: Factory, query_executor: QueryExecutor
) -> None:
    result: Success[list[Product]] | Failure = await query_executor.ask(
        GetAvailableProductsQuery(factory_id=factory.id)
    )
    if isinstance(result, Failure):
        await call.message.answer(result.reason)
        return None
    await call.message.edit_caption(
        caption=msg.sell_products_page,
        reply_markup=kb.sell_products(result.data),
    )
    return None


@router.callback_query(SellProductCallback.filter())
@get_factory
async def choose_amount(call: types.CallbackQuery, factory: Factory) -> None:
    await call.answer("skposdf")
