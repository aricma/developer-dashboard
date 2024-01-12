import dataclasses
from typing import List

import pytest

from business_logic.burn_down_forecaster import (
    BurnDownForecaster,
    Task,
)
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.types import StoryPoints
from business_logic.date_skipper import NoDateSkipper, WeekendSkipper
from business_logic.utils import make_date

TODAY = make_date(2020, 1, 1)
TOMORROW = make_date(2020, 1, 2)
THREE_DAYS_AGO = make_date(2019, 12, 29)
TWO_DAYS_AGO = make_date(2019, 12, 30)
YESTERDAY = make_date(2019, 12, 31)


@dataclasses.dataclass
class ForecastBurnDownForTaskTestCase:
    message: str
    task: Task
    developer_velocity_as_story_points_per_day: StoryPoints
    expected_forecast: BurnDownForecast


test_cases: List[ForecastBurnDownForTaskTestCase] = [
    ForecastBurnDownForTaskTestCase(
        message="Given a task started today with a developer velocity same as the tasks story points,"
        "when called then forecasts the task to be done by today",
        task=Task(
            id="1",
            start_date=TODAY,
            story_points=3,
        ),
        developer_velocity_as_story_points_per_day=3,
        expected_forecast={TODAY: 0},
    ),
    ForecastBurnDownForTaskTestCase(
        message="Given a task started today with a developer velocity higher then the tasks story points,"
        "when called then forecasts the task to be done by today",
        task=Task(
            id="1",
            start_date=TODAY,
            story_points=3,
        ),
        developer_velocity_as_story_points_per_day=4,
        expected_forecast={TODAY: 0},
    ),
    ForecastBurnDownForTaskTestCase(
        message="Given a tasks started today with a developer velocity lower then the tasks story points,"
        "when called then forecasts the task to be done by tomorrow",
        task=Task(
            id="1",
            start_date=TODAY,
            story_points=6,
        ),
        developer_velocity_as_story_points_per_day=3,
        expected_forecast={TODAY: 3, TOMORROW: 0},
    ),
    ForecastBurnDownForTaskTestCase(
        message="Given a tasks started today with a developer velocity much lower then the tasks story points,"
        "when called then returns expected long forecast",
        task=Task(
            id="1",
            start_date=TODAY,
            story_points=32,
        ),
        developer_velocity_as_story_points_per_day=6,
        expected_forecast={
            TODAY: 26,
            TOMORROW: 20,
            make_date(2020, 1, 3): 14,
            make_date(2020, 1, 4): 8,
            make_date(2020, 1, 5): 2,
            make_date(2020, 1, 6): 0,
        },
    ),
    ForecastBurnDownForTaskTestCase(
        message="Given a tasks started 3 days in the past "
        "with a developer velocity much lower then the tasks story points,"
        "when called then returns expected long forecast "
        "from past over today til the expected forecasted end",
        task=Task(
            id="1",
            start_date=THREE_DAYS_AGO,
            story_points=32,
        ),
        developer_velocity_as_story_points_per_day=6,
        expected_forecast={
            THREE_DAYS_AGO: 26,
            TWO_DAYS_AGO: 20,
            YESTERDAY: 14,
            TODAY: 8,
            TOMORROW: 2,
            make_date(2020, 1, 3): 0,
        },
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[each.message for each in test_cases]
)
def test__forecast_burn_down_for_task(
    test_case: ForecastBurnDownForTaskTestCase,
) -> None:
    brun_down_fore_caster = BurnDownForecaster(date_skipper=NoDateSkipper())
    forcast = brun_down_fore_caster.forcast(
        task=test_case.task,
        developer_velocity_as_story_points_per_day=test_case.developer_velocity_as_story_points_per_day,
    )
    assert forcast == test_case.expected_forecast


def test__forecast_burn_down_for_task_with_weekend_skipper() -> None:
    test_case = ForecastBurnDownForTaskTestCase(
        message="Given a tasks started on given today with a developer velocity much lower then the tasks story points,"
        "when called with injected WeekendSkipper then returns expected long forecast",
        task=Task(
            id="1",
            start_date=TODAY,
            story_points=32,
        ),
        developer_velocity_as_story_points_per_day=6,
        expected_forecast={
            TODAY: 26,
            TOMORROW: 20,
            make_date(2020, 1, 3): 14,
            make_date(2020, 1, 6): 8,
            make_date(2020, 1, 7): 2,
            make_date(2020, 1, 8): 0,
        },
    )
    brun_down_fore_caster = BurnDownForecaster(date_skipper=WeekendSkipper())
    forcast = brun_down_fore_caster.forcast(
        task=test_case.task,
        developer_velocity_as_story_points_per_day=test_case.developer_velocity_as_story_points_per_day,
    )
    assert forcast == test_case.expected_forecast
