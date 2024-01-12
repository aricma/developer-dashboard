import dataclasses
from typing import List, Optional

TaskID = str
Date = str
StoryPoints = float
DeveloperID = str


@dataclasses.dataclass
class Task:
    id: TaskID
    story_points: StoryPoints
    assignees: List[DeveloperID]
    sub_tasks: List["Task"]
    date_started: Date
    date_finished: Optional[Date] = None
