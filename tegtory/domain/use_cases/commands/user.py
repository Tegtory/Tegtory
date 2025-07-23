import dataclasses

from tegtory.domain.commands.user import (
    RegisterUserCommand,
    StartUserWorkCommand,
)
from tegtory.domain.entities import User
from tegtory.domain.entities.factory import StartFactoryEvent
from tegtory.domain.entities.user import RegisterUser
from tegtory.domain.events import EventType
from tegtory.domain.interfaces import EventBus, UserRepository
from tegtory.domain.use_cases.commands.base import BaseCommandHandler


@dataclasses.dataclass(frozen=True)
class RegisterUserCommandHandler(BaseCommandHandler[RegisterUserCommand]):
    repo: UserRepository

    async def execute(self, cmd: RegisterUserCommand) -> User | None:
        return await self.repo.create(
            RegisterUser(id=cmd.user_id, name=cmd.name, username=cmd.username)
        )


@dataclasses.dataclass(frozen=True)
class StartUserWorkCommandHandler(BaseCommandHandler[StartUserWorkCommand]):
    repo: UserRepository
    event_bus: EventBus

    async def execute(self, cmd: StartUserWorkCommand) -> None:
        cmd.user.can_start_work()
        await self.repo.start_work(cmd.user.id, cmd.time)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=cmd.factory, time=cmd.time, product=cmd.product
            ),
        )
