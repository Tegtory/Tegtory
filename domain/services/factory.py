from common import settings
from common.exceptions import AppError, TaxError
from domain.entities import Factory
from domain.use_cases.base import DependencyRequired


class FactoryService(DependencyRequired):
    @staticmethod
    def hire_worker(factory: Factory) -> Factory:
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
