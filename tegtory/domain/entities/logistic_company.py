import dataclasses

from tegtory.domain.entities.contract import BaseContract
from tegtory.domain.entities.factory import Factory, Product
from tegtory.domain.entities.shop import Shop
from tegtory.domain.entities.user import User


@dataclasses.dataclass(kw_only=True, frozen=True)
class LogisticContract(BaseContract):
    product: Product
    amount: float
    destination: Shop
    price_km: float
    factory: Factory
    company: "LogisticCompany"


@dataclasses.dataclass(kw_only=True, frozen=True)
class Transport:
    name: str
    speed: float
    price: float
    max_size: float
    max_weight: float


@dataclasses.dataclass(kw_only=True, frozen=True)
class LogisticCompanyTransport:
    transport: Transport
    company: "LogisticCompany"
    amount: int = 1


@dataclasses.dataclass(kw_only=True)
class LogisticCompany:
    id: int
    title: str
    description: str
    owner: User | None = None
    is_bot: bool = True
