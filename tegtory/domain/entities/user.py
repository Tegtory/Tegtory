import dataclasses
import math
import time

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
class User:
    id: int
    money: float = 500
    stolar: int = 0
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
