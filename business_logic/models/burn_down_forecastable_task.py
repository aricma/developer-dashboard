import dataclasses

TaskID = str
StoryPoints = float
Date = str


@dataclasses.dataclass
class BurnDownForecastableTask:
    id: TaskID
    story_points: StoryPoints
    date_started: Date
