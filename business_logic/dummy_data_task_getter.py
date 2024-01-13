import json
from pathlib import Path
from typing import List, Optional, Dict

from business_logic.errors import DummyDataNotFoundError
from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.date import Date
from business_logic.models.task import Task
from business_logic.serializer.dummy_data_file_de_serializer import (
    DeserializedDummyTasksFile,
)
from business_logic.serializer.task import DeserializedTask

TaskID = str


class DummyDataTaskGetter(TaskGetter[Task]):
    def __init__(
        self,
        path_to_dummy_data_tasks_file: str,
    ):
        self._path_to_dummy_data_tasks = path_to_dummy_data_tasks_file

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self._normalize_tasks(tasks=self.get_tasks()).get(task_id)

    @staticmethod
    def _normalize_tasks(tasks: List[Task]) -> Dict[TaskID, Task]:
        return {task.id: task for task in tasks}

    def get_tasks(self) -> List[Task]:
        deserialized_dummy_data_file = self._read_dummy_data()
        return self._to_tasks(deserialized_dummy_data_file.tasks)

    def _to_tasks(self, deserialized_tasks: List[DeserializedTask]) -> List[Task]:
        return [
            self._to_task(deserialized_task) for deserialized_task in deserialized_tasks
        ]

    def _to_task(self, deserialized_task: DeserializedTask):
        return Task(
            id=deserialized_task.id,
            name=deserialized_task.title,
            description=deserialized_task.description,
            story_points=deserialized_task.story_points,
            assignees=deserialized_task.assignees,
            sub_tasks=self._to_tasks(deserialized_task.sub_tasks),
            date_started=Date.from_string(deserialized_task.date_started),
            date_finished=(
                Date.from_string(deserialized_task.date_finished)
                if deserialized_task.date_finished is not None
                else None
            ),
        )

    def _read_dummy_data(self) -> DeserializedDummyTasksFile:
        file_path_to_dummy_data = Path(self._path_to_dummy_data_tasks)
        if file_path_to_dummy_data.exists() and file_path_to_dummy_data.is_file():
            return DeserializedDummyTasksFile(
                **self._read_json_file_content(file_path_to_dummy_data)
            )
        raise DummyDataNotFoundError()

    @staticmethod
    def _read_json_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return json.loads(reader.read())
