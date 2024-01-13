from typing import List, Optional

from pydantic import BaseModel

TaskID = str
DeveloperID = str
Date = str


class DeserializedTask(BaseModel):
    id: TaskID
    title: str
    description: str
    story_points: float
    assignees: List[DeveloperID]
    sub_tasks: List["DeserializedTask"]
    date_started: Date
    date_finished: Optional[Date] = None
