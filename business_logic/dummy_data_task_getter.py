import glob
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
FileName = str


class DummyDataTaskGetter(TaskGetter[Task]):
    def __init__(
        self,
        path_to_dummy_data: str,
    ):
        self._path_to_dummy_data = path_to_dummy_data

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self._normalize_tasks(tasks=self.get_tasks()).get(task_id)

    def get_tasks(self) -> List[Task]:
        all_file_names = self._get_all_dummy_data_file_names()
        all_deserialized_dummy_data_files = self._read_all_dummy_data(
            file_names=all_file_names
        )
        result: List[Task] = []
        for deserialized_dummy_data_file in all_deserialized_dummy_data_files:
            for deserialized_task in deserialized_dummy_data_file.tasks:
                result.append(self._to_task(deserialized_task))
        return result

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

    def _read_all_dummy_data(
        self, file_names: List[str]
    ) -> List[DeserializedDummyTasksFile]:
        return [self._read_dummy_data(Path(file_name)) for file_name in file_names]

    def _read_dummy_data(self, file: Path) -> DeserializedDummyTasksFile:
        if file.exists() and file.is_file():
            return DeserializedDummyTasksFile(**self._read_json_file_content(file))
        raise DummyDataNotFoundError()

    def _get_all_dummy_data_file_names(self) -> List[str]:
        return glob.glob(self._path_to_dummy_data + "/*.json")

    @staticmethod
    def _normalize_tasks(tasks: List[Task]) -> Dict[TaskID, Task]:
        return {task.id: task for task in tasks}

    @staticmethod
    def _read_json_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return json.loads(reader.read())
