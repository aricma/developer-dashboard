# The burn down metric show how many days, weeks, months until a task is done
import dataclasses
from datetime import timedelta
from math import ceil
from typing import List, Optional

from humanize import naturaldelta


@dataclasses.dataclass
class Task:
    id: str
    name: str
    link: str
    story_points: Optional[int]


@dataclasses.dataclass
class BurnDownMetric:
    id: str
    name: str
    link: str
    done_in: str  # representation of remaining years, months, weeks, and days


class OldBurnDownTracker:

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
            id="1",
            name="epic-1",
            link="https://...",
            story_points=34,
        ),
        Task(
            id="2",
            name="task-1",
            link="https://...",
            story_points=5,
        ),
        Task(
            id="3",
            name="bug-3",
            link="https://...",
            story_points=None,
        ),
        Task(
            id="4",
            name="spike-4",
            link="https://...",
            story_points=5,
        ),
        Task(
            id="5",
            name="spike-5",
            link="https://...",
            story_points=12,
        )
    ]

    bdt = OldBurnDownTracker(developer_velocity_per_day=2)

    for each in tasks:
        bdt.add_task(each)

    for each in bdt.get_all():
        print(each)
