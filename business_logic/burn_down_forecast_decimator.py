from itertools import islice

from business_logic.interfaces.decimator import Decimator
from business_logic.models.burn_down_forecast import BurnDownForecast


class BurnDownForecastDecimator(Decimator[BurnDownForecast]):
    def __init__(self, max_amount_of_data_points_per_forecast: int):
        self._max_amount_of_data_points_per_forecast = (
            max_amount_of_data_points_per_forecast
        )

    def decimate(self, forecast: BurnDownForecast) -> BurnDownForecast:
        if len(forecast) > self._max_amount_of_data_points_per_forecast:
            return self._decimate(forecast)
        return forecast

    def _decimate(self, forecast: BurnDownForecast) -> BurnDownForecast:
        length_of_forecast = len(forecast)
        start_index = 0
        stop_index = length_of_forecast
        steps = int(length_of_forecast / self._max_amount_of_data_points_per_forecast)
        down_sampled = islice(forecast.items(), start_index, stop_index, steps)
        return {date: story_points for date, story_points in down_sampled}
