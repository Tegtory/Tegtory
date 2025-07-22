from tegtory.common import settings
from tegtory.common.exceptions import AppError, TaxError
from tegtory.domain.entities import Factory
from tegtory.domain.use_cases.base import DependencyRequired


class FactoryService(DependencyRequired):
    @staticmethod
    def hire(factory: Factory) -> Factory:
        if factory.hire_available == 0:
            raise AppError("Максимальное количество рабочих достигнуто")
        factory.hire()
        return factory

    @staticmethod
    def start(factory: Factory, time: float) -> None:
        if factory.state:
            return
        if factory.workers == 0:
            raise AppError("Нельзя запустить фабрику без рабочих")
        if factory.tax > settings.TAX_LIMIT:
            raise TaxError
        factory.start_work(time)
