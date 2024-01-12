import dataclasses
import json
from pathlib import Path
from typing import Union, List

from business_logic.chart_data_formatter import (
    ChartDataFormatter,
    VelocityChartDataFile,
)
from business_logic.developer_velocity_tracker import DeveloperVelocityTracker
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.dummy_data_task_getter import DummyDataTaskGetter
from business_logic.models.velocity_trackable_task import VelocityTrackableTask
from business_logic.serializer.misc import Account
from business_logic.utils import hash_string_value
from business_logic.velocity_trackable_task_getter_proxy import (
    VelocityTrackableTaskGetterProxy,
)
from server.constants import PATH_TO_STATIC_FILES


class DeveloperVelocityBusinessLogic:
    def __init__(self, path_to_tasks_json_file: str):
        self._task_getter = VelocityTrackableTaskGetterProxy(
            task_getter=DummyDataTaskGetter(
                path_to_dummy_data_tasks_file=path_to_tasks_json_file
            )
        )
        self._velocity_tracker = DeveloperVelocityTracker()
        self._chart_data_formatter = ChartDataFormatter()

    def get_velocity_data_file_name_for_developer(
        self, account: Account, time_in_weeks: int
    ) -> str:
        data = self._get_velocity_data_for_developer(
            account=account, time_in_weeks=time_in_weeks
        )
        return self.get_file_path_for_data(
            data=dataclasses.asdict(data), account_id=account.id
        )

    def get_file_path_for_data(self, data: dict, account_id: str) -> str:
        formatted_data = self._pretty_format_json(data)
        file_name = self._make_velocity_data_file_name_for_developer(
            developer_id=account_id, data_finger_print=hash_string_value(formatted_data)
        )
        if not self._static_file_does_exist(file_name):
            self._write_velocity_data_to_file(file_name, formatted_data)
        return file_name

    def get_average_developer_velocity(self) -> DeveloperVelocity:
        tracking_start_date = Date.today().go_back_weeks(weeks=8)
        tasks = self._filter_tasks_before_given_start_date(
            tasks=self._task_getter.get_tasks(),
            start_date=tracking_start_date,
        )
        return self._velocity_tracker.track_average_developer_velocity(tasks=tasks)

    def _get_velocity_data_for_developer(
        self, account: Account, time_in_weeks: int
    ) -> VelocityChartDataFile:
        tracking_start_date = Date.today().go_back_weeks(weeks=time_in_weeks)
        tasks = self._filter_tasks_before_given_start_date(
            tasks=self._task_getter.get_tasks(),
            start_date=tracking_start_date,
        )
        developer_velocity_data = self._velocity_tracker.track_developer_velocity(
            tasks=tasks,
            tracked_developer=account.name,
        )
        average_developer_velocity_data = (
            self._velocity_tracker.track_average_developer_velocity(tasks=tasks)
        )
        return self._chart_data_formatter.to_single_developer_velocity_chart_data(
            developer_velocity=self._filter_velocity_before_given_start_date(
                velocity=developer_velocity_data,
                start_date=tracking_start_date,
            ),
            average_developer_velocity=self._filter_velocity_before_given_start_date(
                velocity=average_developer_velocity_data,
                start_date=tracking_start_date,
            ),
        )

    @staticmethod
    def _filter_tasks_before_given_start_date(
        tasks: List[VelocityTrackableTask], start_date: Date
    ) -> List[VelocityTrackableTask]:
        return [task for task in tasks if task.date_finished >= start_date]

    @staticmethod
    def _filter_velocity_before_given_start_date(
        velocity: DeveloperVelocity, start_date: Date
    ) -> DeveloperVelocity:
        return {
            date: story_points
            for date, story_points in velocity.items()
            if Date.from_string(date) >= start_date
        }

    @staticmethod
    def _pretty_format_json(value: Union[dict, list]) -> str:
        return json.dumps(value, indent=4, sort_keys=True)

    @staticmethod
    def _make_velocity_data_file_name_for_developer(
        developer_id: str, data_finger_print: str
    ) -> str:
        return f"{developer_id}-velocity-data-{data_finger_print}.json"

    def _static_file_does_exist(self, file_name: str) -> bool:
        return self._file_does_exist(str(PATH_TO_STATIC_FILES / file_name))

    @staticmethod
    def _file_does_exist(path: str) -> bool:
        return Path(path).exists() and Path(path).is_file()

    def _write_velocity_data_to_file(self, file_name: str, data: str) -> None:
        self._write_data_to_file(path=str(PATH_TO_STATIC_FILES / file_name), data=data)

    @staticmethod
    def _write_data_to_file(path: str, data: str) -> None:
        with open(path, "w") as writer:
            writer.write(data)
