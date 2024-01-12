from datetime import timedelta as duration
from dateutil.parser import parse as to_date

from business_logic.date_skipper import DateSkipper
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.burn_down_forecastable_task import BurnDownForecastableTask

Date = str


class BurnDownForecaster:
    def __init__(self, date_skipper: DateSkipper):
        self._date_skipper = date_skipper

    def forcast(
        self, task: BurnDownForecastableTask, developer_velocity_as_story_points_per_day: float
    ) -> BurnDownForecast:
        story_points_per_day = developer_velocity_as_story_points_per_day
        remaining_task_story_points = task.story_points
        next_date = task.date_started
        forecast: BurnDownForecast = {}

        while remaining_task_story_points > 0:
            if not self._date_skipper.date_should_be_skipped(next_date):
                remaining_task_story_points = (
                    remaining_task_story_points - story_points_per_day
                )
                if remaining_task_story_points < 0:
                    forecast[next_date] = 0
                else:
                    forecast[next_date] = remaining_task_story_points

            next_date = self._increase_date_by_one_day(date=next_date)

        return forecast

    @staticmethod
    def _increase_date_by_one_day(date: Date) -> Date:
        return str((to_date(date) + duration(days=1)).date())
