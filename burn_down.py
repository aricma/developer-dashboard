# The burn down metric show how many days, weeks, months until a task is done
import dataclasses
from datetime import timedelta
from enum import Enum
from math import ceil
from typing import List, Optional

from humanize import naturaldelta


class TaskType(Enum):
    EPIC = "EPIC"
    USER_STORY = "USER_STORY"
    TASK = "TASK"
    SPIKE = "SPIKE"
    BUG = "BUG"


@dataclasses.dataclass
class Task:
    type: TaskType
    id: str
    name: str
    link: str
    story_points: Optional[int]


@dataclasses.dataclass
class BurnDownMetric:
    type: TaskType
    id: str
    name: str
    link: str
    done_in: str  # representation of remaining years, months, weeks, and days


class BurnDownTracker:

    _metrics: List[BurnDownMetric]
    _developer_velocity_per_day: int

    def __init__(self, developer_velocity_per_day: int):
        self._developer_velocity_per_day = developer_velocity_per_day
        self._metrics = list()

    def get_all(self) -> List[BurnDownMetric]:
        return self._metrics

    def add_task(self, task: Task) -> None:
        if task.story_points is None:
            done_in = "infinite time"
        else:
            done_in = naturaldelta(
                timedelta(days=ceil(task.story_points / self._developer_velocity_per_day))
            )
        metric = BurnDownMetric(
            type=task.type,
            id=task.id,
            name=task.name,
            link=task.link,
            done_in=done_in
        )
        self._metrics.append(metric)


if __name__ == '__main__':
    # api = ...
    # project = api.get_project("AK")
    # tasks = project.tasks()

    tasks = [
        Task(
            type=TaskType.EPIC,
            id="1",
            name="epic-1",
            link="https://...",
            story_points=34,
        ),
        Task(
            type=TaskType.TASK,
            id="2",
            name="task-1",
            link="https://...",
            story_points=5,
        ),
        Task(
            type=TaskType.BUG,
            id="3",
            name="bug-3",
            link="https://...",
            story_points=None,
        ),
        Task(
            type=TaskType.SPIKE,
            id="4",
            name="spike-4",
            link="https://...",
            story_points=5,
        ),
        Task(
            type=TaskType.USER_STORY,
            id="5",
            name="spike-5",
            link="https://...",
            story_points=12,
        )
    ]

    bdt = BurnDownTracker(developer_velocity_per_day=2)

    for each in tasks:
        bdt.add_task(each)

    for each in bdt.get_all():
        print(each)
