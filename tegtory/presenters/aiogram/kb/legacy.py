from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu_kb = [
    [KeyboardButton(text="Фабрика"), KeyboardButton(text="Город")],
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Биржа")],
]
menu_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=menu_kb)

old_seasons_kb = [
    [
        InlineKeyboardButton(
            text="Сезон pre-alpha", callback_data="pre_apha_season"
        )
    ],
    [InlineKeyboardButton(text="Сезон alpha", callback_data="alpha_season")],
    [InlineKeyboardButton(text="Обратно", callback_data="leaderboard")],
]
old_seasons_markup = InlineKeyboardMarkup(inline_keyboard=old_seasons_kb)

back_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обратно", callback_data="city")]
    ]
)

back_exchange = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="рынок")]
    ]
)
