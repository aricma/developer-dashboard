import dataclasses
from typing import List

from business_logic.interfaces.decimator import Decimator
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.models.story_points import EstimatedStoryPoints

Date = str
StoryPoints = float


@dataclasses.dataclass
class VelocityChartDataPoint:
    x: Date
    y: StoryPoints


VelocityChartDataPoints = List[VelocityChartDataPoint]


@dataclasses.dataclass
class VelocityChartData:
    developer_velocity: VelocityChartDataPoints
    average_developer_velocity: VelocityChartDataPoints


@dataclasses.dataclass
class VelocityChartDataFile:
    data_points: VelocityChartData


@dataclasses.dataclass
class BurnDownChartDataPointMetaData:
    estimated: bool


@dataclasses.dataclass
class BurnDownChartDataPoint:
    x: Date
    y: StoryPoints
    meta: BurnDownChartDataPointMetaData


@dataclasses.dataclass
class BurnDownChartDataFile:
    data_points: List[BurnDownChartDataPoint]


class ChartDataFormatter:
    def __init__(
        self,
        burn_down_forecast_decimator: Decimator[BurnDownForecast],
        developer_velocity_decimator: Decimator[DeveloperVelocity],
    ):
        self._burn_down_forecast_decimator = burn_down_forecast_decimator
        self._developer_velocity_decimator = developer_velocity_decimator

    def to_single_developer_velocity_chart_data(
        self,
        developer_velocity: DeveloperVelocity,
        average_developer_velocity: DeveloperVelocity,
    ) -> VelocityChartDataFile:
        decimated_developer_velocity = self._developer_velocity_decimator.decimate(
            developer_velocity
        )
        decimated_average_developer_velocity = (
            self._developer_velocity_decimator.decimate(average_developer_velocity)
        )
        return VelocityChartDataFile(
            data_points=VelocityChartData(
                developer_velocity=self.sort_data_points_by_date(
                    data_points=self.velocity_to_chart_data_points(
                        velocity=decimated_developer_velocity
                    ),
                ),
                average_developer_velocity=self.sort_data_points_by_date(
                    data_points=self.velocity_to_chart_data_points(
                        velocity=decimated_average_developer_velocity
                    ),
                ),
            )
        )

    def to_burn_down_chart_data(
        self,
        burn_down_forecast: BurnDownForecast,
    ) -> BurnDownChartDataFile:
        decimated_burn_down_forecast = self._burn_down_forecast_decimator.decimate(
            burn_down_forecast
        )
        return BurnDownChartDataFile(
            data_points=[
                BurnDownChartDataPoint(
                    x=date,
                    y=story_points.value,
                    meta=BurnDownChartDataPointMetaData(
                        estimated=isinstance(story_points, EstimatedStoryPoints),
                    ),
                )
                for date, story_points in decimated_burn_down_forecast.items()
            ]
        )

    @staticmethod
    def velocity_to_chart_data_points(
        velocity: DeveloperVelocity,
    ) -> VelocityChartDataPoints:
        return [
            VelocityChartDataPoint(
                x=date,
                y=story_points,
            )
            for date, story_points in velocity.items()
        ]

    @staticmethod
    def sort_data_points_by_date(
        data_points: VelocityChartDataPoints,
    ) -> VelocityChartDataPoints:
        return sorted(data_points, key=lambda data_point: data_point.x)
