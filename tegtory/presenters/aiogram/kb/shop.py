from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tegtory.domain.entities import Shop, ShopProduct
from tegtory.presenters.aiogram.kb.callbacks import CityCB


def get_shop_markup(shop: Shop) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=shop.title, callback_data=f"{CityCB.shop}:{shop.title}"
    )
    builder.button(
        text="Товары", callback_data=f"{CityCB.choose_product}:{shop.title}"
    )
    builder.button(text="Обратно", callback_data=CityCB.shop)
    return builder.as_markup()


def get_shop_list_markup(shops: list[Shop]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.max_width = 2

    for shop in shops:
        builder.button(
            text=shop.title, callback_data=f"{CityCB.shop}:{shop.title}"
        )
    builder.adjust(1, repeat=True)
    builder.row(
        InlineKeyboardButton(
            text="Без доставки",
            callback_data=f"{CityCB.shop}-ListShopNoDeliveryQuery",
        ),
        InlineKeyboardButton(
            text="Требуется доставка",
            callback_data=f"{CityCB.shop}-ListShopDeliveryQuery",
        ),
    )
    builder.button(text="Очистить", callback_data=CityCB.shop)
    builder.button(text="назад", callback_data=CityCB.back)
    return builder.as_markup()


def shop_demand_markup(products: list[ShopProduct]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=f"{product.product.name} - {product.amount}",
            callback_data=f"{CityCB.choose_amount}:{product.id}",
        )
    builder.adjust(2, repeat=True)
    builder.button(text="назад", callback_data=CityCB.shop)

    return builder.as_markup()


def choose_amount_demand_markup(product: ShopProduct) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for available_amount in get_steps_markup(product):
        builder.button(
            text=str(available_amount),
            callback_data=f"{CityCB.preview_contract}:{product.shop.title}:{product.product.name}:{available_amount}",
        )
    builder.adjust(4, repeat=True)
    builder.button(
        text="назад", callback_data=f"{CityCB.shop}:{product.shop.title}"
    )
    return builder.as_markup()


def get_steps_markup(product: ShopProduct) -> list[int]:
    return [
        i
        for i in range(
            product.amount // 10,
            product.amount // 2,
            int(product.amount * 0.05) + 1,
        )
    ]


prices = [LabeledPrice(label="1000 очков XTR", amount=10)]
