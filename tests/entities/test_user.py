import time

from tegtory.domain.entities import User


def test_user_minutes_to_work() -> None:
    user = User(id=1, name="", username="")
    user.end_work_time = time.time() + 60
    less_minute = 0.99
    assert less_minute <= user.minutes_to_work <= 1.0


def test_user_set_name() -> None:
    user = User(id=1, name="", username="")
    user.set_name("lol")
    assert user.name == "lol"


def test_user_can_buy() -> None:
    user = User(id=1, name="", username="")
    user.money = 100
    assert user.can_buy(100)


def test_user_cannot_buy() -> None:
    user = User(id=1, name="", username="")
    user.money = 0
    assert not user.can_buy(100)
