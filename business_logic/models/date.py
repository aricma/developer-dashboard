from dateutil import parser
import datetime


class Date:
    def __init__(self, year: int, month: int, day: int):
        self._year = year
        self._month = month
        self._day = day

    def from_string(self, date_as_string: str) -> "Date":
        parsed_date = parser.parse(date_as_string)
        return self.from_datetime_date(datetime_date=parsed_date)

    @staticmethod
    def from_datetime_date(datetime_date: datetime.date) -> "Date":
        return Date(
            year=datetime_date.year,
            month=datetime_date.month,
            day=datetime_date.day,
        )

    def to_string(self) -> str:
        return f"{self._year}-{self._month}-{self._day}"

    def to_datetime_date(self) -> datetime.date:
        return datetime.date(
            year=self._year,
            month=self._month,
            day=self._day,
        )

    def add_days(self, days: int) -> "Date":
        return ...

    def is_weekend(self) -> bool:
        return self.to_datetime_date().weekday() > 4  # 5 & 6 are Sat and Sun
