import statistics

from business_logic.burn_down_forecastable_task_aggregator import (
    BurnDownForecastableTaskAggregator,
)
from business_logic.burn_down_forecastable_task_getter_proxy import (
    BurnDownForecastableTaskGetterProxy,
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
from business_logic.dummy_data_task_getter import DummyDataTaskGetter
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.uuid_maker import UUIDMaker

StoryPoints = float


class BurnDownBusinessLogic:
    def __init__(self, path_to_tasks_json_file: str):
        self._velocity_bs = DeveloperVelocityBusinessLogic(
            path_to_tasks_json_file=path_to_tasks_json_file
        )
        self._task_getter = BurnDownForecastableTaskGetterProxy(
            task_getter=DummyDataTaskGetter(
                path_to_dummy_data_tasks_file=path_to_tasks_json_file
            )
        )
        self._burn_down_forecaster = BurnDownForecaster(
            date_skipper=NoDateSkipper(),
            # date_skipper=WeekendSkipper(),
            date_classifier=DateClassifier(today=Date.today()),
        )
        self._task_aggregator = BurnDownForecastableTaskAggregator(id_maker=UUIDMaker())

    def get_task_burn_down_data_for_account(self) -> BurnDownForecast:
        tasks = self._task_getter.get_tasks()
        aggregated_task = self._task_aggregator.aggregate(tasks)
        return self._burn_down_forecaster.forcast(
            task=aggregated_task,
            developer_velocity_as_story_points_per_day=self._get_average_developer_velocity(),
        )

    def _get_average_developer_velocity(self) -> StoryPoints:
        return self._get_mean_developer_velocity(
            developer_velocity=self._velocity_bs.get_average_developer_velocity(
                time_in_weeks=8
            )
        )

    @staticmethod
    def _get_mean_developer_velocity(developer_velocity: DeveloperVelocity) -> float:
        return statistics.median(developer_velocity.values())
