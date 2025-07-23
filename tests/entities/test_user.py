import time

from tegtory.domain.entities import User


def test_user_minutes_to_work() -> None:
    user = User(id=1, end_work_time=time.time() + 60)
    less_minute = 0.99
    assert less_minute <= user.minutes_to_work <= 1.0
