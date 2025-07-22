import dataclasses


@dataclasses.dataclass(frozen=True)
class Success[T]:
    data: T


@dataclasses.dataclass(frozen=True)
class Failure:
    reason: str
