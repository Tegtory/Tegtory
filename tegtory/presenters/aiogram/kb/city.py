from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tegtory.domain.entities.logistic_company import LogisticCompany
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
        InlineKeyboardButton(text="Магазины", callback_data=CityCB.shop),
    ],
]
city_markup = InlineKeyboardMarkup(inline_keyboard=city_kb)


def trading_company(companies: list[LogisticCompany]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in companies:
        builder.button(
            text=i.title, callback_data=f"{CityCB.trading_companies}:{i.id}"
        )
    builder.button(text="Обратно", callback_data=CityCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()
