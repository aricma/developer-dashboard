import dataclasses
from typing import List

import pytest

from business_logic.burn_down_forecast_decimator import BurnDownForecastDecimator
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.date import Date
from business_logic.models.story_points import StoryPoints, EstimatedStoryPoints


@dataclasses.dataclass
class BurnDownForecastDecimatorTestCase:
    message: str
    decimation_threshold: int
    given_burn_down_forecast: BurnDownForecast
    expected_decimated_burn_down_forecast: BurnDownForecast


test_cases: List[BurnDownForecastDecimatorTestCase] = [
    BurnDownForecastDecimatorTestCase(
        message="Given forcast with less data points than set DECIMATION_THRESHOLD,"
        "when called then returns given forcast",
        decimation_threshold=5,
        given_burn_down_forecast={
            Date(2020, 1, 1).to_string(): StoryPoints(3),
            Date(2020, 1, 2).to_string(): StoryPoints(2),
            Date(2020, 1, 3).to_string(): EstimatedStoryPoints(1),
            Date(2020, 1, 4).to_string(): EstimatedStoryPoints(0),
        },
        expected_decimated_burn_down_forecast={
            Date(2020, 1, 1).to_string(): StoryPoints(3),
            Date(2020, 1, 2).to_string(): StoryPoints(2),
            Date(2020, 1, 3).to_string(): EstimatedStoryPoints(1),
            Date(2020, 1, 4).to_string(): EstimatedStoryPoints(0),
        },
    ),
    BurnDownForecastDecimatorTestCase(
        message="Given forcast with same amount of data points as set DECIMATION_THRESHOLD,"
        "when called then returns given forcast",
        decimation_threshold=5,
        given_burn_down_forecast={
            Date(2019, 12, 31).to_string(): StoryPoints(4),
            Date(2020, 1, 1).to_string(): StoryPoints(3),
            Date(2020, 1, 2).to_string(): StoryPoints(2),
            Date(2020, 1, 3).to_string(): EstimatedStoryPoints(1),
            Date(2020, 1, 4).to_string(): EstimatedStoryPoints(0),
        },
        expected_decimated_burn_down_forecast={
            Date(2019, 12, 31).to_string(): StoryPoints(4),
            Date(2020, 1, 1).to_string(): StoryPoints(3),
            Date(2020, 1, 2).to_string(): StoryPoints(2),
            Date(2020, 1, 3).to_string(): EstimatedStoryPoints(1),
            Date(2020, 1, 4).to_string(): EstimatedStoryPoints(0),
        },
    ),
]


@pytest.mark.parametrize("test_case", test_cases, ids=[tc.message for tc in test_cases])
def test__decimate(test_case: BurnDownForecastDecimatorTestCase) -> None:
    decimator = BurnDownForecastDecimator(
        max_amount_of_data_points_per_forecast=test_case.decimation_threshold
    )
    result = decimator.decimate(test_case.given_burn_down_forecast)
    assert test_case.expected_decimated_burn_down_forecast == result
