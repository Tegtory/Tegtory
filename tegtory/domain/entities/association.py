import dataclasses

from tegtory.domain.entities.user import User


@dataclasses.dataclass(kw_only=True, frozen=True)
class Association:
    title: str
    description: str
    owner: User


@dataclasses.dataclass(kw_only=True)
class AssociationParticipant:
    association: Association
    participant: User
    role: str
    contributed: int = 0
