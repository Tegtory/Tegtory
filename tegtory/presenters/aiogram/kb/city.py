from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tegtory.domain.entities import Product
from tegtory.presenters.aiogram.kb.callbacks import CityCB

back_city_button = InlineKeyboardButton(
    text="Обратно", callback_data=CityCB.back
)

city_kb = [
    [InlineKeyboardButton(text="Зал славы", callback_data=CityCB.leaderboard)],
    [
        InlineKeyboardButton(
            text="Торговые компании", callback_data=CityCB.trading_companies
        ),
        InlineKeyboardButton(
            text="Сбыт продукции", callback_data=CityCB.sell_product
        ),
    ],
]
city_markup = InlineKeyboardMarkup(inline_keyboard=city_kb)


def sell_products(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in products:
        builder.button(
            text=f"{i.name}, цена за ед. {i.price_multiply}",
            callback_data=f"{CityCB.sell_product}:{i.name}",
        )
    builder.button(text="Обратно", callback_data=CityCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()
