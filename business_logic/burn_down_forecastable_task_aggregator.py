from typing import List

from business_logic.interfaces.maker import Maker
from business_logic.interfaces.task_aggregator import TaskAggregator
from business_logic.models.burn_down_forecastable_task import BurnDownForecastableTask
from business_logic.models.date import Date

StoryPoints = float


class BurnDownForecastableTaskAggregator(TaskAggregator[BurnDownForecastableTask]):
    def __init__(self, id_maker: Maker[str]):
        self._id_maker = id_maker

    def aggregate(
        self, tasks: List[BurnDownForecastableTask]
    ) -> BurnDownForecastableTask:
        return BurnDownForecastableTask(
            id=self._id_maker.make(),
            story_points=self._get_all_story_points(tasks),
            date_started=self._get_earliest_date(tasks),
        )

    @staticmethod
    def _get_all_story_points(tasks: List[BurnDownForecastableTask]) -> StoryPoints:
        all_story_points: float = 0
        for task in tasks:
            all_story_points += task.story_points
        return all_story_points

    def _get_earliest_date(self, tasks: List[BurnDownForecastableTask]) -> Date:
        if len(tasks) == 0:
            return self._make_fallback_date()
        first_task = tasks[0]
        earliest_date: Date = first_task.date_started
        for task in tasks:
            if task.date_started < earliest_date:
                earliest_date = task.date_started
        return earliest_date

    @staticmethod
    def _make_fallback_date() -> Date:
        return Date.today()
