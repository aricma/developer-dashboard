from business_logic.models.date import Date


class DateClassifier:

    def __init__(self, today: Date):
        self._today = today

    def is_future(self, date: Date) -> bool:
        return self._today <= date
