from collections.abc import Callable

from aiogram import F, Router, types

from tegtory.presenters.aiogram.filters.city import CityFilter
from tegtory.presenters.aiogram.images import Images
from tegtory.presenters.aiogram.kb import CityCB
from tegtory.presenters.aiogram.kb import city as kb
from tegtory.presenters.aiogram.messages import city as msg
from tegtory.presenters.shared.utils import cache, get_factory

router = Router()


@router.message(CityFilter())
@cache(Images.city, types.FSInputFile(Images.city))
async def city_page(
    message: types.Message,
    cached: types.FSInputFile | str,
    cache_func: Callable,
) -> None:
    sent = await message.answer_photo(
        photo=cached, caption=msg.main, reply_markup=kb.city_markup
    )
    if sent.photo:
        cache_func(sent.photo[-1].file_id)


@router.callback_query(F.data == CityCB.back)
async def city_callback(call: types.CallbackQuery) -> None:
    await call.message.edit_caption(
        caption=msg.main, reply_markup=kb.city_markup
    )


@router.callback_query(F.data == CityCB.trading_companies)
@get_factory
async def trading_companies_page(call: types.CallbackQuery) -> None:
    await call.message.edit_caption(caption=msg.main)
