from abc import ABC, abstractmethod

from business_logic.models.date import Date


class DateSkipper(ABC):
    @abstractmethod
    def date_should_be_skipped(self, date: Date) -> bool:
        ...


class NoDateSkipper(DateSkipper):
    def date_should_be_skipped(self, _: Date) -> bool:
        return False


class WeekendSkipper(DateSkipper):
    def date_should_be_skipped(self, date: Date) -> bool:
        return date.is_weekend()
