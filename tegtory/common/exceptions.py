class AppError(Exception):
    message = ""

    def __init__(self, message: str = "") -> None:
        if message:
            self.message = message


class NotEnoughPointsError(AppError):
    message = "Недостаточно очков"


class TaxError(AppError):
    message = "Выплатите Налоги чтобы продолжить"


class DuringWorkError(AppError):
    message = "Невозможно выполнить действие во время работы"


class FactoryRequiredError(AppError):
    message = "Для выполнения действия необходима фабрика"
