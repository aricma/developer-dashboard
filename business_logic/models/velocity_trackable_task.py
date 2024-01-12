import dataclasses
from typing import List

TaskID = str
StoryPoints = float
DeveloperID = str
Date = str


@dataclasses.dataclass
class VelocityTrackableTask:
    id: TaskID
    story_points: StoryPoints
    assignees: List[DeveloperID]
    date_started: Date
    date_finished: Date
