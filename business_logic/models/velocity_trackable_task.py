import dataclasses
from typing import List

from business_logic.models.date import Date

TaskID = str
StoryPoints = float
DeveloperID = str


@dataclasses.dataclass
class VelocityTrackableTask:
    id: TaskID
    story_points: StoryPoints
    assignees: List[DeveloperID]
    date_started: Date
    date_finished: Date
