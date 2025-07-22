from .base import BaseQuery


class ListShopQuery(BaseQuery):
    pass


class ListShopNoDeliveryQuery(BaseQuery):
    pass


class ListShopDeliveryQuery(BaseQuery):
    pass


class ShopQuery(BaseQuery):
    title: str
