from datetime import timedelta as duration
from dateutil import parser
import datetime


class Date:
    def __init__(self, year: int, month: int, day: int):
        self._year = year
        self._month = month
        self._day = day

    def __gt__(self, other: "Date") -> bool:
        return self.to_datetime_date() > other.to_datetime_date()

    def __lt__(self, other: "Date") -> bool:
        return self.to_datetime_date() < other.to_datetime_date()

    def __eq__(self, other):
        return self.to_datetime_date() == other.to_datetime_date()

    def __le__(self, other):
        return self.to_datetime_date() <= other.to_datetime_date()

    def __ge__(self, other):
        return self.to_datetime_date() >= other.to_datetime_date()

    @staticmethod
    def today() -> "Date":
        return Date.from_datetime_date(datetime.date.today())

    @staticmethod
    def from_datetime_date(datetime_date: datetime.date) -> "Date":
        return Date(
            year=datetime_date.year,
            month=datetime_date.month,
            day=datetime_date.day,
        )

    @staticmethod
    def from_string(date_as_string: str) -> "Date":
        parsed_date = parser.parse(date_as_string)
        return Date.from_datetime_date(datetime_date=parsed_date)

    def to_string(self) -> str:
        return f"{self._year}-{self._month}-{self._day}"

    def to_datetime_date(self) -> datetime.date:
        return datetime.date(
            year=self._year,
            month=self._month,
            day=self._day,
        )

    def add_days(self, days: int) -> "Date":
        return self.from_datetime_date(self.to_datetime_date() + duration(days=days))

    def go_back_weeks(self, weeks: int) -> "Date":
        return self.from_datetime_date(self.to_datetime_date() - duration(weeks=weeks))

    def is_weekend(self) -> bool:
        return self.to_datetime_date().weekday() > 4  # 5 & 6 are Sat and Sun

    def get_days_until(self, next_date: "Date") -> int:
        return (self.to_datetime_date() - next_date.to_datetime_date()).days
