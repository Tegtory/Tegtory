import dataclasses
import math
import time
from uuid import UUID

from tegtory.common.exceptions import DuringWorkError


@dataclasses.dataclass(kw_only=True, frozen=True)
class Dignity:
    name: str
    user: "User"


@dataclasses.dataclass(kw_only=True, frozen=True)
class RegisterUser:
    id: int
    username: str
    name: str = ""


@dataclasses.dataclass(kw_only=True, frozen=True)
class Wallet:
    owner_id: UUID
    stolar: int = 0
    money: float = 500


@dataclasses.dataclass(kw_only=True, frozen=True)
class User:
    iternal_id: UUID | None = None
    id: int
    end_work_time: float = 0

    @property
    def minutes_to_work(self) -> float:
        return float(math.ceil(self.work_time_remaining / 60 * 10) / 10)

    @property
    def work_time_remaining(self) -> float:
        return self.end_work_time - time.time()

    @property
    def state(self) -> bool:
        return self.work_time_remaining > 0.0

    def can_start_work(self) -> None:
        if self.state:
            raise DuringWorkError
