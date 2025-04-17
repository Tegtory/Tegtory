from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.entity.factory import Product

from .callbacks import FactoryCB
from .utils import one_inline_button_markup


def get_choose_product_markup(mode: str, products: list[Product]):
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=product.name,
            callback_data=f"{FactoryCB.choose_time}:{mode}:{product.name}:",
        )
    builder.button(text="Обратно", callback_data=FactoryCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def get_time_choose_markup(mode: str, product: Product):
    builder = InlineKeyboardBuilder()
    timestamps = [
        [5, 300],
        [15, 900],
        [30, 1800],
        [45, 2700],
        [60, 3600],
        [120, 7200],
    ]

    for timestamp in timestamps:
        amount = timestamp[1] // product.time_to_create
        builder.button(
            text=f"{timestamp[0]} минут 🟰 {amount} ед.",
            callback_data=f"{mode}:{product.name}:{timestamp[1]}",
        )
    builder.button(text="Обратно", callback_data=FactoryCB.back)
    builder.adjust(1, repeat=True)
    return builder.as_markup()


back_button = InlineKeyboardButton(
    text="Обратно", callback_data=FactoryCB.back
)
back_markup = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

create_markup = one_inline_button_markup("Создать фабрику", FactoryCB.create)

factory_kb = [
    [
        InlineKeyboardButton(
            text="Работать", callback_data=FactoryCB.work_yourself
        ),
        InlineKeyboardButton(
            text="Запустить фабрику", callback_data=FactoryCB.start
        ),
    ],
    [
        InlineKeyboardButton(
            text="Улучшение", callback_data=FactoryCB.upgrade
        ),
        InlineKeyboardButton(
            text="Работники", callback_data=FactoryCB.workers
        ),
    ],
    [
        InlineKeyboardButton(text="Налоги", callback_data=FactoryCB.tax),
        InlineKeyboardButton(text="Склад", callback_data=FactoryCB.storage),
    ],
]
main = InlineKeyboardMarkup(inline_keyboard=factory_kb)

hire_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Нанять", callback_data=FactoryCB.hire)],
        [back_button],
    ]
)

failed_hire_markup = one_inline_button_markup("обратно", FactoryCB.workers)

upgrade_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="улучшить", callback_data=FactoryCB.upgrade_conf
            )
        ],
        [back_button],
    ]
)

failed_upgrade_markup = one_inline_button_markup(
    text="Обратно", callback_data=FactoryCB.upgrade
)

tax_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатить налоги", callback_data=FactoryCB.pay_tax
            )
        ],
        [back_button],
    ]
)

storage_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Улучшить склад", callback_data=FactoryCB.upgrade_storage
            )
        ],
        [back_button],
    ]
)
