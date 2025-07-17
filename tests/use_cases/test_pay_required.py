import pytest

from tegtory.common.exceptions import AppError
from tegtory.domain.use_cases.commands.pay_required import pay_required


def test_pay_required_failure_exec() -> None:
    cls = type("", (), {})
    with pytest.raises(AppError):
        pay_required(cls)
