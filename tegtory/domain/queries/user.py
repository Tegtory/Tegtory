from .base import BaseQuery


class UserQuery(BaseQuery):
    user_id: int


class WalletQuery(UserQuery):
    pass
