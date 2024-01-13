from typing import Union

from business_logic.interfaces.date_skipper import DateSkipper
from business_logic.date_classifier import DateClassifier
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.burn_down_forecastable_task import BurnDownForecastableTask
from business_logic.models.date import Date
from business_logic.models.story_points import StoryPoints, EstimatedStoryPoints


class BurnDownForecaster:
    def __init__(self, date_skipper: DateSkipper, date_classifier: DateClassifier):
        self._date_skipper = date_skipper
        self._date_classifier = date_classifier

    def forcast(
        self,
        task: BurnDownForecastableTask,
        developer_velocity_as_story_points_per_day: float,
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
                forecast[next_date.to_string()] = self._get_story_points(
                    next_date=next_date,
                    remaining_task_story_points=remaining_task_story_points,
                )
            next_date = next_date.add_days(days=1)

        return forecast

    def _get_story_points(
        self,
        next_date: Date,
        remaining_task_story_points: float,
    ) -> Union[StoryPoints, EstimatedStoryPoints]:
        value = self._get_next_value(
            remaining_task_story_points=remaining_task_story_points
        )
        if self._date_classifier.is_future(next_date):
            return EstimatedStoryPoints(value)
        else:
            return StoryPoints(value)

    @staticmethod
    def _get_next_value(remaining_task_story_points: float) -> float:
        if remaining_task_story_points < 0:
            return 0
        else:
            return remaining_task_story_points
