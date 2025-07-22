from typing import Any

from aiogram import Router, types

from tegtory.domain import entities, results
from tegtory.domain.commands import StartUserWorkCommand
from tegtory.domain.commands.factory import StartFactoryCommand
from tegtory.domain.entities import Factory, Product
from tegtory.domain.events import EventType
from tegtory.domain.queries.factory import (
    GetAvailableProductsQuery,
    GetSpecificProductQuery,
)
from tegtory.domain.results import Failure, Success
from tegtory.infrastructure import CommandExecutor, QueryExecutor
from tegtory.infrastructure.injectors import on_event
from tegtory.presenters.aiogram.filters.factory import (
    ChooseProductFilter,
    ChooseTimeToWorkFilter,
    StartFactoryFilter,
    StartYourselfFactoryFilter,
)
from tegtory.presenters.aiogram.handlers.factory.main import callback_factory
from tegtory.presenters.aiogram.kb import factory as kb
from tegtory.presenters.aiogram.messages import factory as msg
from tegtory.presenters.aiogram.utils import get_factory
from tegtory.presenters.bot import TegtorySingleton

router = Router()


@router.callback_query(ChooseProductFilter())
@get_factory
async def choose_product(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    query_executor: QueryExecutor,
) -> Any:
    can_start = await check_can_start_factory(user, factory)
    if can_start:
        return await call.answer(can_start, show_alert=True)
    result: Success[list[Product]] | Failure = await query_executor.ask(
        GetAvailableProductsQuery(factory_id=factory.id)
    )
    if isinstance(result, Failure):
        return await call.answer(result.reason, show_alert=True)
    markup = kb.get_choose_product_markup(str(call.data), result.data)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )


async def check_can_start_factory(
    user: entities.User, factory: entities.Factory
) -> str | None:
    result = None
    if factory.state:
        result = msg.start_factory_work.format(factory.minutes_to_work)
    elif user.state:
        result = msg.start_yourself_work.format(user.minutes_to_work)
    return result


@router.callback_query(ChooseTimeToWorkFilter())
@get_factory
async def choose_time(
    call: types.CallbackQuery, factory: Factory, query_executor: QueryExecutor
) -> None:
    mode = call.data.split(":")[1]
    product: Success[Product] | Failure = await query_executor.ask(
        GetSpecificProductQuery(
            factory_id=factory.id, name=call.data.split(":")[2]
        )
    )
    if isinstance(product, Failure):
        await call.answer(product.reason)
        return
    markup = kb.get_time_choose_markup(mode, product.data)
    await call.message.edit_caption(
        caption=msg.choose_product, reply_markup=markup
    )
    return


@router.callback_query(StartYourselfFactoryFilter())
@get_factory
async def work_yourself(
    call: types.CallbackQuery,
    user: entities.User,
    factory: entities.Factory,
    cmd_executor: CommandExecutor,
    query_executor: QueryExecutor,
) -> Any:
    product, time = await get_product_time(call, factory, query_executor)
    if not product or not time:
        await call.answer("Вам недоступен этот продукт")
        return
    result = await cmd_executor.execute(
        StartUserWorkCommand(
            user=user,
            product=product,
            time=time,
            factory=factory,
        )
    )
    if isinstance(result, results.Success):
        await callback_factory(call)
        return
    await call.answer(result.reason, show_alert=True)


@router.callback_query(StartFactoryFilter())
@get_factory
async def start_factory(
    call: types.CallbackQuery,
    factory: Factory,
    cmd_executor: CommandExecutor,
    query_executor: QueryExecutor,
) -> Any:
    product, time = await get_product_time(call, factory, query_executor)
    if not product or not time:
        await call.answer("Вам недоступен этот продукт")
        return
    result: Success[Factory] | Failure = await cmd_executor.execute(
        StartFactoryCommand(factory=factory, time=time, product=product)
    )
    if isinstance(result, Success):
        await call.answer(str(result.data), show_alert=True)
        return
    await callback_factory(call)


@on_event(EventType.EndFactoryWork)
async def end_factory_work(data: dict[str, Factory | int]) -> None:
    factory = data.get("factory")
    stock = data.get("stock")
    if not isinstance(factory, Factory) or not isinstance(stock, int):
        return
    bot = TegtorySingleton()
    await bot.send_message(factory.id, msg.success_work_end.format(stock))


async def get_product_time(
    call: types.CallbackQuery,
    factory: Factory,
    query_executor: QueryExecutor,
) -> tuple[Product, float] | tuple[None, None]:
    result = await query_executor.ask(
        GetSpecificProductQuery(
            factory_id=factory.id, name=call.data.split(":")[1]
        )
    )
    if isinstance(result, Failure):
        return None, None
    return result.data, float(call.data.split(":")[2])
