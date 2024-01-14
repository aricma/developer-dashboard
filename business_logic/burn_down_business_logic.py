import statistics
from typing import List, Optional

from business_logic.burn_down_forecastable_task_aggregator import (
    BurnDownForecastableTaskAggregator,
)
from business_logic.burn_down_forecaster import BurnDownForecaster
from business_logic.date_classifier import DateClassifier
from business_logic.interfaces.date_skipper import (
    NoDateSkipper,
    # WeekendSkipper
)
from business_logic.developer_velocity_business_logic import (
    DeveloperVelocityBusinessLogic,
)
from business_logic.dummy_data_task_getter import DummyDataFileTaskGetter
from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.burn_down_forecastable_task import BurnDownForecastableTask
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.models.task import Task
from business_logic.uuid_maker import UUIDMaker

StoryPoints = float


class BurnDownBusinessLogic:
    def __init__(
        self,
        developer_velocity_business_logic: DeveloperVelocityBusinessLogic,
        dummy_data_file_task_getter: DummyDataFileTaskGetter,
        burn_down_forecastable_task_getter: TaskGetter[BurnDownForecastableTask],
    ):
        self._velocity_bs = developer_velocity_business_logic
        self._dummy_data_task_getter = dummy_data_file_task_getter
        self._task_getter = burn_down_forecastable_task_getter
        self._burn_down_forecaster = BurnDownForecaster(
            date_skipper=NoDateSkipper(),
            # date_skipper=WeekendSkipper(),
            date_classifier=DateClassifier(today=Date.today()),
        )
        self._task_aggregator = BurnDownForecastableTaskAggregator(id_maker=UUIDMaker())

    def get_all_burn_down_forecastable_tasks(self) -> List[Task]:
        return [
            task
            for task in self._dummy_data_task_getter.get_tasks()
            if task.date_finished is None
        ]

    def get_total_task_burn_down_data(self) -> BurnDownForecast:
        tasks = self._task_getter.get_tasks()
        aggregated_task = self._task_aggregator.aggregate(tasks)
        return self._burn_down_forecaster.forcast(
            task=aggregated_task,
            developer_velocity_as_story_points_per_day=self._get_average_developer_velocity(),
        )

    def get_task_burn_down_data(
        self, task_id: str, developer_velocity_as_story_points_per_day: float
    ) -> Optional[BurnDownForecast]:
        task = self._task_getter.get_task_by_id(task_id)
        if task is not None:
            return self._burn_down_forecaster.forcast(
                task=task,
                developer_velocity_as_story_points_per_day=developer_velocity_as_story_points_per_day,
            )
        return None

    def _get_average_developer_velocity(self) -> StoryPoints:
        return self._get_median_developer_velocity(
            developer_velocity=self._velocity_bs.get_average_developer_velocity(
                time_in_weeks=8
            )
        )

    @staticmethod
    def _get_median_developer_velocity(developer_velocity: DeveloperVelocity) -> float:
        return statistics.median(developer_velocity.values())
