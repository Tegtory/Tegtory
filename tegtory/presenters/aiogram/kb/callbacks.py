from enum import EnumType

from aiogram.filters.callback_data import CallbackData


class CityCB(EnumType):
    back = "city"
    shop = "city__shop"
    sell_product = "city__sell_product"
    search_shop = "city__search_shop"
    choose_product = "city_shop__choose_product"
    choose_amount = "city_shop__choose_amount"
    preview_contract = "city_shop__preview_contract"
    success_contract = "city_shop__success_contract"
    leaderboard = "city__leaderboard"
    trading_companies = "city__trading_companies"


class FactoryCB(EnumType):
    back = "factory"
    create = "factory__create"
    choose_time = "factory_time"
    work_yourself = "factory_yourself"
    start = "factory_start"
    upgrade = "factory_upgrade"
    upgrade_conf = "factory_upgrade:pay"
    tax = "factory_tax"
    pay_tax = "factory_tax:pay"
    storage = "factory_storage"
    upgrade_storage = "factory_storage:pay"
    workers = "factory_workers"
    hire = "factory_workers:pay"


class OtherCB(EnumType):
    working_on = "other__working_on"
    subscribe = "other__subscribe"
    balance = "other__balance"


class SellProductCallback(CallbackData, prefix=CityCB.sell_product):
    name: str
