import dataclasses
from typing import Set, Union, Literal, List

Permissions = Set[Union[Literal["READ_ALL", "READ_MINE", "READ_AND_WRITE_ALL"]]]

TaskID = str
DeveloperID = str
Date = str


@dataclasses.dataclass
class FinishedTask:
    id: TaskID
    date_started: Date
    date_finished: Date
    story_points: float
    assignees: List[DeveloperID]
