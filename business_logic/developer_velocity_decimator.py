from itertools import islice

from business_logic.interfaces.decimator import Decimator
from business_logic.models.developer_velocity import DeveloperVelocity


class DeveloperVelocityDecimator(Decimator[DeveloperVelocity]):
    def __init__(self, max_amount_of_data_points_per_velocity: int):
        self._max_amount_of_data_points_per_velocity = (
            max_amount_of_data_points_per_velocity
        )

    def decimate(self, velocity: DeveloperVelocity) -> DeveloperVelocity:
        if len(velocity) > self._max_amount_of_data_points_per_velocity:
            return self._decimate(velocity)
        return velocity

    def _decimate(self, velocity: DeveloperVelocity) -> DeveloperVelocity:
        length_of_forecast = len(velocity)
        start_index = 0
        stop_index = length_of_forecast
        steps = int(length_of_forecast / self._max_amount_of_data_points_per_velocity)
        down_sampled = islice(velocity.items(), start_index, stop_index, steps)
        return {date: story_points for date, story_points in down_sampled}
