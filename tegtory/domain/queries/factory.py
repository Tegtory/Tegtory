from .base import BaseQuery


class BaseFactoryQuery(BaseQuery):
    factory_id: int


class GetFactoryQuery(BaseFactoryQuery):
    pass


class GetFactoryByName(BaseQuery):
    factory_name: str


class GetStorageQuery(BaseFactoryQuery):
    pass


class GetAvailableProductsQuery(BaseFactoryQuery):
    pass


class GetSpecificProductQuery(BaseFactoryQuery):
    name: str
