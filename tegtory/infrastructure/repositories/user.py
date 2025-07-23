import logging
from time import time

from grpc import aio, ssl_channel_credentials
from grpc.aio import AioRpcError
from redis.asyncio import Redis

import tegtory.auth_pb2 as proto
from tegtory.auth_pb2_grpc import AuthServiceStub
from tegtory.common.exceptions import NotEnoughPointsError
from tegtory.common.settings import settings
from tegtory.domain.entities import User
from tegtory.domain.entities.user import RegisterUser
from tegtory.domain.interfaces import UserRepository

logger = logging.getLogger(__name__)


class RedisUserRepositoryImpl(UserRepository):
    def __init__(self) -> None:
        self.redis = Redis(
            settings.REDIS_HOST,
            settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        channel = aio.secure_channel(
            settings.USER_MICROSERVICE_URL, ssl_channel_credentials()
        )
        self.client = AuthServiceStub(channel)  # type: ignore

    async def get(self, item_id: int) -> User | None:
        result = self.redis.hgetall(f"user:{item_id}")
        if result:
            return User(
                id=item_id,
                end_work_time=float(result.get("end_work_time")),
                money=float(result.get("money")),
                stolar=int(result.get("stolar")),
            )
        try:
            user = await self.client.login_telegram(
                proto.LoginUser(telegram_id=item_id),
                metadata=(("auth", settings.USER_MICROSERVICE_KEY),),
            )
        except AioRpcError:
            return None
        cache_user = User(id=item_id)
        await self.redis.hset(
            f"user:{item_id}",
            mapping={
                "id": user.id,
                "end_work_time": cache_user.end_work_time,
                "money": cache_user.money,
                "stolar": cache_user.stolar,
            },
        )
        return cache_user

    async def create(self, user: RegisterUser) -> User:
        logger.info(f"Creating user {user.id} with name {user.name}")
        await self.client.register_telegram(
            proto.AuthUser(
                name=user.name, username=user.username, telegram_id=user.id
            ),
            metadata=(("auth", settings.USER_MICROSERVICE_KEY),),
        )
        return User(id=user.id)

    async def subtract(self, user_id: int, amount: float) -> None:
        balance = float(self.redis.hget(f"user:{user_id}", "money"))
        if balance < amount:
            raise NotEnoughPointsError
        await self.redis.hset(
            f"user:{user_id}", "money", str(balance - amount)
        )

    async def add(self, user_id: int, amount: float) -> None:
        balance = float(self.redis.hget(f"user:{user_id}", "money"))
        await self.redis.hset(
            f"user:{user_id}", "money", str(balance + amount)
        )

    async def start_work(self, user_id: int, amount: float) -> None:
        await self.redis.hset(
            f"user:{user_id}", "end_work_time", str(time() + amount)
        )
