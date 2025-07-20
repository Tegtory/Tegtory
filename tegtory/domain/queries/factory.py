from .base import BaseQuery


class GetFactoryQuery(BaseQuery):
    factory_id: int


class GetFactoryByName(BaseQuery):
    factory_name: str


class GetStorageQuery(BaseQuery):
    factory_id: int


class GetAvailableProductsQuery(BaseQuery):
    factory_id: int
