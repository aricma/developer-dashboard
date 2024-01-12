from abc import ABC, abstractmethod

from dateutil.parser import parse as to_date

Date = str


class DateSkipper(ABC):
    @abstractmethod
    def date_should_be_skipped(self, date: Date) -> bool:
        ...


class NoDateSkipper(DateSkipper):
    def date_should_be_skipped(self, _: Date) -> bool:
        return False


class WeekendSkipper(DateSkipper):
    def date_should_be_skipped(self, date: Date) -> bool:
        return to_date(date).weekday() > 4  # 5 & 6 are Sat and Sun
