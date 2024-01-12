import dataclasses

from business_logic.models.date import Date

TaskID = str
StoryPoints = float


@dataclasses.dataclass
class BurnDownForecastableTask:
    id: TaskID
    story_points: StoryPoints
    date_started: Date
