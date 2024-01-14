import dataclasses
import glob
import json
from pathlib import Path
from typing import List, Optional, Dict, Set

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
DeveloperID = str
StoryPoints = float


@dataclasses.dataclass
class NormalizedTask:
    """
    This is an internal model of the DummyDataFileTaskGetter
    """

    id: TaskID
    name: str
    description: str
    story_points: StoryPoints
    assignees: List[DeveloperID]
    sub_task_ids: List[TaskID]
    date_started: Date
    date_finished: Optional[Date] = None


class DummyDataFileTaskGetter(TaskGetter[Task]):
    _files_read: Set[FileName]
    _normalized_parsed_tasks: Dict[TaskID, NormalizedTask]

    def __init__(
        self,
        path_to_dummy_data: str,
    ):
        self._path_to_dummy_data = path_to_dummy_data
        self._files_read = set()
        self._normalized_parsed_tasks = {}
        self._update_parsed_data()

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        self._update_parsed_data()
        normalized_task = self._normalized_parsed_tasks.get(task_id)
        return self._to_task(normalized_task) if normalized_task is not None else None

    def get_tasks(self) -> List[Task]:
        self._update_parsed_data()
        sub_task_ids: Set[TaskID] = set()
        for task in self._normalized_parsed_tasks.values():
            for task_id in task.sub_task_ids:
                sub_task_ids.add(task_id)
        return [
            self._to_task(task)
            for task in self._normalized_parsed_tasks.values()
            if task.id not in sub_task_ids
        ]

    def _update_parsed_data(self) -> None:
        all_file_names = self._get_all_dummy_data_file_names()
        all_deserialized_dummy_data_files = self._read_all_dummy_data(
            file_names=all_file_names
        )
        for deserialized_dummy_data_file in all_deserialized_dummy_data_files:
            for deserialized_task in deserialized_dummy_data_file.tasks:
                self._add_deserialized_task(deserialized_task)

    def _add_deserialized_task(self, deserialized_task: DeserializedTask) -> None:
        for each in deserialized_task.sub_tasks:
            self._add_deserialized_task(deserialized_task=each)
        parsed_task = self._to_normalized_task(deserialized_task)
        self._normalized_parsed_tasks[parsed_task.id] = parsed_task

    def _get_tasks_for_ids(self, task_ids: List[TaskID]) -> List[Task]:
        result: List[Task] = []
        for task_id in task_ids:
            normalized_task = self._normalized_parsed_tasks.get(task_id)
            if normalized_task is not None:
                self._to_task(normalized_task)
        return result

    def _read_all_dummy_data(
        self, file_names: List[str]
    ) -> List[DeserializedDummyTasksFile]:
        result: List[DeserializedDummyTasksFile] = []
        for file_name in file_names:
            if file_name not in self._files_read:
                result.append(self._read_dummy_data(Path(file_name)))
                self._files_read.add(file_name)
        return result

    def _read_dummy_data(self, file: Path) -> DeserializedDummyTasksFile:
        if file.exists() and file.is_file():
            return DeserializedDummyTasksFile(**self._read_json_file_content(file))
        raise DummyDataNotFoundError()

    def _get_all_dummy_data_file_names(self) -> List[str]:
        return glob.glob(self._path_to_dummy_data + "/*.json")

    @staticmethod
    def _to_normalized_task(deserialized_task: DeserializedTask) -> NormalizedTask:
        return NormalizedTask(
            id=deserialized_task.id,
            name=deserialized_task.title,
            description=deserialized_task.description,
            story_points=deserialized_task.story_points,
            assignees=deserialized_task.assignees,
            sub_task_ids=[task.id for task in deserialized_task.sub_tasks],
            date_started=Date.from_string(deserialized_task.date_started),
            date_finished=(
                Date.from_string(deserialized_task.date_finished)
                if deserialized_task.date_finished is not None
                else None
            ),
        )

    def _to_task(self, normalized_task: NormalizedTask) -> Task:
        return Task(
            id=normalized_task.id,
            name=normalized_task.name,
            description=normalized_task.description,
            story_points=normalized_task.story_points,
            assignees=normalized_task.assignees,
            sub_tasks=self._get_tasks_for_ids(task_ids=normalized_task.sub_task_ids),
            date_started=normalized_task.date_started,
            date_finished=normalized_task.date_finished,
        )

    @staticmethod
    def _read_json_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return json.loads(reader.read())
