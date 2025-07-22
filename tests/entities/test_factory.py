import time

import pytest

from tegtory.common.exceptions import DuringWorkError
from tegtory.domain.entities import Factory


def test_factory_minutes_to_work() -> None:
    factory = Factory(id=1, name="")
    factory.end_work_time = time.time() + 60
    less_minute = 0.99
    assert less_minute <= factory.minutes_to_work <= 1.0


def test_upgrade_price() -> None:
    factory = Factory(id=1, name="")
    factory.level = 0
    assert factory.upgrade_price == (factory.level + 2) * 370


def test_start_work() -> None:
    factory = Factory(id=1, name="")
    result = factory.start_work(10)
    assert result > time.time()


def test_not_start_work() -> None:
    factory = Factory(id=1, name="")
    final_time = time.time() + 60
    factory.end_work_time = final_time
    factory.start_work(10)
    assert factory.end_work_time == final_time


def test_hire_failure() -> None:
    factory = Factory(id=1, name="")
    final_time = time.time() + 60
    factory.end_work_time = final_time

    with pytest.raises(DuringWorkError):
        factory.hire()


def test_rename() -> None:
    factory = Factory(id=1, name="")
    factory.rename("new_name")
    assert factory.name == "new_name"


def test_set_tax() -> None:
    factory = Factory(id=1, name="")
    tax = 100
    factory.set_tax(tax)
    assert factory.tax != tax
