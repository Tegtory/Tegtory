import logging
from collections.abc import Awaitable
from time import time

from grpc import aio, ssl_channel_credentials
from grpc.aio import AioRpcError
from redis.asyncio import Redis

import tegtory.auth_pb2 as proto
from tegtory import money_pb2 as money_proto
from tegtory.auth_pb2_grpc import AuthServiceStub
from tegtory.common.settings import settings
from tegtory.domain.entities import User
from tegtory.domain.entities.user import RegisterUser, Wallet
from tegtory.domain.interfaces import UserRepository
from tegtory.domain.interfaces.user import WalletRepository
from tegtory.money_pb2_grpc import MoneyServiceStub

logger = logging.getLogger(__name__)


class RedisUserRepositoryImpl(UserRepository):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        channel = aio.secure_channel(
            settings.USER_MICROSERVICE_URL, ssl_channel_credentials()
        )
        self.client = AuthServiceStub(channel)  # type: ignore

    async def get(self, item_id: int) -> User | None:
        result = self.redis.hgetall(f"user:{item_id}")
        if isinstance(result, Awaitable):
            result = await result
        if result:
            end_work_time = result.get("end_work_time", "0.0")
            if not isinstance(end_work_time, str):
                return None
            return User(
                iternal_id=result.get("id"),
                id=item_id,
                end_work_time=float(end_work_time),
            )
        try:
            user = await self.client.login_telegram(
                proto.LoginUser(telegram_id=item_id),
                metadata=(("auth", settings.USER_MICROSERVICE_KEY),),
            )
        except AioRpcError as e:
            logger.error(str(e))
            return None
        cache_user = User(id=item_id, iternal_id=user.id)
        self.redis.hset(
            f"user:{item_id}",
            mapping={
                "id": user.id,
                "end_work_time": cache_user.end_work_time,
            },
        )
        self.redis.expire(f"user:{item_id}", 1800)
        return cache_user

    async def create(self, user: RegisterUser) -> User:
        logger.info(f"Creating user {user.id} with name {user.name}")
        result = await self.client.register_telegram(
            proto.AuthUser(
                name=user.name, username=user.username, telegram_id=user.id
            ),
            metadata=(("auth", settings.USER_MICROSERVICE_KEY),),
        )
        return User(id=user.id, iternal_id=result.id)

    async def start_work(self, user_id: int, amount: float) -> None:
        self.redis.hset(
            f"user:{user_id}", "end_work_time", str(time() + amount)
        )


class WalletRepositoryImpl(WalletRepository):
    def __init__(self, user_repo: UserRepository) -> None:
        channel = aio.secure_channel(
            settings.WALLET_SERVICE_URL, ssl_channel_credentials()
        )
        self.client = MoneyServiceStub(channel)  # type: ignore

        self.user_repo = user_repo

    async def get(self, tgid: int) -> Wallet | None:
        user = await self.user_repo.get(tgid)
        logger.info(f"getting wallet for {user=}")
        if not user or not user.iternal_id:
            return None
        wallet = await self.client.balance(
            money_proto.User(id=user.iternal_id),
            metadata=settings.money_metadata,
        )
        logger.info(f"received wallet {wallet=}")
        return Wallet(
            owner_id=user.iternal_id, stolar=0, money=float(wallet.balance)
        )

    async def charge(self, tgid: int, amount: float) -> bool:
        user = await self.user_repo.get(tgid)
        if not user:
            return False
        result = await self.client.charge(
            money_proto.ChargeUser(id=user.iternal_id, money=amount),
            metadata=settings.money_metadata,
        )
        return bool(result == money_proto.status.STATUS_SUCCESSFULLY)

    async def add(self, tgid: int, amount: float) -> None:
        user = await self.user_repo.get(tgid)
        if not user:
            return
        await self.client.add(
            money_proto.ChargeUser(id=user.iternal_id, money=amount),
            metadata=settings.money_metadata,
        )
