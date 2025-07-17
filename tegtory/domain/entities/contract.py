import dataclasses
from datetime import datetime
from enum import Enum


class ContractStatus(Enum):
    CREATED = "created"
    DELIVERED = "delivered"
    FINISHED = "finished"
    EXPIRED = "expired"


@dataclasses.dataclass(kw_only=True, frozen=True)
class BaseContract:
    id: int
    status: ContractStatus
    estimated_date: datetime
    created_at: datetime = dataclasses.field(default_factory=datetime.now)
