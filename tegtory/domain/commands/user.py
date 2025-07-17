from ..entities import Factory, Product, User
from .base import BaseCommand


class RegisterUserCommand(BaseCommand):
    username: str
    name: str
    user_id: int


class StartUserWorkCommand(BaseCommand):
    user: User
    time: float
    product: Product
    factory: Factory
