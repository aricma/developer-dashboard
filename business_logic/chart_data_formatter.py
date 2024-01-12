import dataclasses
from typing import List

from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.developer_velocity import DeveloperVelocity

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
    def to_single_developer_velocity_chart_data(
            self,
            developer_velocity: DeveloperVelocity,
            average_developer_velocity: DeveloperVelocity,
    ) -> VelocityChartDataFile:
        return VelocityChartDataFile(
            data_points=VelocityChartData(
                developer_velocity=self.sort_data_points_by_date(
                    data_points=self.velocity_to_chart_data_points(
                        velocity=developer_velocity
                    ),
                ),
                average_developer_velocity=self.sort_data_points_by_date(
                    data_points=self.velocity_to_chart_data_points(
                        velocity=average_developer_velocity
                    ),
                ),
            )
        )

    @staticmethod
    def to_burn_down_chart_data(burn_down_forecast: BurnDownForecast) -> BurnDownChartDataFile:
        return BurnDownChartDataFile(
            data_points=[
                BurnDownChartDataPoint(
                    x=date,
                    y=story_points,
                    meta=BurnDownChartDataPointMetaData(
                        estimated=True,
                    )
                )
                for date, story_points in burn_down_forecast.items()
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
