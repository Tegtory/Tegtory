from enum import Enum


class EventType(Enum):
    StartFactory = "start_factory"
    EndFactoryWork = "end_factory_work"
    UpgradeFactory = "start_upgrade_factory"
    SubtractMoney = "subtract_money"
