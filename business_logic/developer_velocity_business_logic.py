import json
from pathlib import Path
from typing import Union, List

from business_logic.developer_velocity_tracker import DeveloperVelocityTracker
from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.models.velocity_trackable_task import VelocityTrackableTask
from business_logic.serializer.misc import Account
from business_logic.utils import hash_string_value
from server.constants import PATH_TO_STATIC_FILES


class DeveloperVelocityBusinessLogic:
    def __init__(self, task_getter: TaskGetter[VelocityTrackableTask]):
        self._task_getter = task_getter
        self._velocity_tracker = DeveloperVelocityTracker()

    def get_developer_velocity(
        self, account: Account, time_in_weeks: int
    ) -> DeveloperVelocity:
        return self._velocity_tracker.track_developer_velocity(
            tasks=self._get_tasks(time_in_weeks=time_in_weeks),
            tracked_developer=account.name,
        )

    def get_average_developer_velocity(self, time_in_weeks: int) -> DeveloperVelocity:
        return self._velocity_tracker.track_average_developer_velocity(
            tasks=self._get_tasks(time_in_weeks=time_in_weeks)
        )

    def _get_tasks(self, time_in_weeks: int) -> List[VelocityTrackableTask]:
        tracking_start_date = Date.today().go_back_weeks(weeks=time_in_weeks)
        return self._filter_tasks_before_given_start_date(
            tasks=self._task_getter.get_tasks(),
            start_date=tracking_start_date,
        )

    def get_file_path_for_data(self, data: dict, account_id: str) -> str:
        formatted_data = self._pretty_format_json(data)
        file_name = self._make_velocity_data_file_name_for_developer(
            developer_id=account_id, data_finger_print=hash_string_value(formatted_data)
        )
        if not self._static_file_does_exist(file_name):
            self._write_velocity_data_to_file(file_name, formatted_data)
        return file_name

    @staticmethod
    def _filter_tasks_before_given_start_date(
        tasks: List[VelocityTrackableTask], start_date: Date
    ) -> List[VelocityTrackableTask]:
        return [task for task in tasks if task.date_finished >= start_date]

    @staticmethod
    def filter_velocity_before_given_start_date(
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
