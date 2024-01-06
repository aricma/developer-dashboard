import dataclasses
from typing import Set, Union, Literal, List

Permissions = Set[Union[Literal["READ_ALL", "READ_MINE", "READ_AND_WRITE_ALL"]]]

TaskID = str
DeveloperID = str
Date = str


@dataclasses.dataclass
class Task:
    id: TaskID
    title: str
    description: str
    date_created: Date
    date_finished: Date
    story_points: int
    assignees: List[DeveloperID]
    subtasks: List[TaskID]


FinishedTask = Task
TaskInProgress = Task
