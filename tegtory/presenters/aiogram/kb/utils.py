from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def one_inline_button_markup(
    text: str, callback_data: str
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
        ]
    )
