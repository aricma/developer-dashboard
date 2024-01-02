# The velocity metric shows how many story points each developer finishes per day
import dataclasses
from datetime import date
from enum import Enum
from math import ceil
from statistics import median
from typing import Dict


class Developer(Enum):
    LT = "Gia Long Tran"
    AM = "Adrian Mindak"
    JB = "Joshua Barrington"
    AN = "Alexey Naumov"
    EE = "Elshafie Eltayeb"


@dataclasses.dataclass
class IssueWithStatusDone:
    assignee: Developer
    start_date: date
    finish_date: date
    story_points: int


@dataclasses.dataclass
class DeveloperVelocity:
    developer: Developer
    story_points_per_day: int


class DeveloperVelocityTracker:

    _velocities: Dict[Developer, DeveloperVelocity]

    def __init__(self):
        self._velocities = dict()

    def get(self, developer: Developer) -> DeveloperVelocity:
        return self._velocities[developer]

    def get_average_velocity(self) -> int:
        return median([each.story_points_per_day for each in self._velocities.values()])

    def add_velocity(self, developer_velocity: DeveloperVelocity) -> None:
        if developer_velocity.developer not in self._velocities:
            self._velocities[developer_velocity.developer] = developer_velocity
        else:
            current_velocity = self._velocities[developer_velocity.developer]
            self._velocities[developer_velocity.developer] = (
                    self._average_velocity(current_velocity, developer_velocity)
            )

    @staticmethod
    def _average_velocity(a: DeveloperVelocity, b: DeveloperVelocity) -> DeveloperVelocity:
        return DeveloperVelocity(
            developer=a.developer,
            story_points_per_day=ceil((a.story_points_per_day + b.story_points_per_day) / 2)
        )


def get_developer_velocity_from_issue(issue: IssueWithStatusDone) -> DeveloperVelocity:
    days = (abs(issue.finish_date - issue.start_date)).days
    days = 1 if days <= 0 else days
    return DeveloperVelocity(
        developer=issue.assignee,
        story_points_per_day=ceil(issue.story_points / days)
    )


if __name__ == '__main__':
    # api = ...
    # issues = api.get_all_isses(
    #     _from=...,
    #     _to=...,
    # )

    issues = [
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=1,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=1,
            ),
            story_points=1
        ),
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=2,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=3,
            ),
            story_points=2
        ),
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=4,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=6,
            ),
            story_points=2
        ),
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=7,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=9,
            ),
            story_points=3
        ),
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=10,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=13,
            ),
            story_points=5
        ),
        IssueWithStatusDone(
            assignee=Developer.AM,
            start_date=date(
                year=2023,
                month=11,
                day=15,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=20,
            ),
            story_points=8
        ),
        ############################################################################
        IssueWithStatusDone(
            assignee=Developer.LT,
            start_date=date(
                year=2023,
                month=11,
                day=1,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=1,
            ),
            story_points=1
        ),
        IssueWithStatusDone(
            assignee=Developer.AN,
            start_date=date(
                year=2023,
                month=11,
                day=2,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=3,
            ),
            story_points=2
        ),
        IssueWithStatusDone(
            assignee=Developer.JB,
            start_date=date(
                year=2023,
                month=11,
                day=4,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=6,
            ),
            story_points=2
        ),
        IssueWithStatusDone(
            assignee=Developer.EE,
            start_date=date(
                year=2023,
                month=11,
                day=7,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=9,
            ),
            story_points=3
        ),
        IssueWithStatusDone(
            assignee=Developer.LT,
            start_date=date(
                year=2023,
                month=11,
                day=10,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=13,
            ),
            story_points=5
        ),
        IssueWithStatusDone(
            assignee=Developer.AN,
            start_date=date(
                year=2023,
                month=11,
                day=15,
            ),
            finish_date=date(
                year=2023,
                month=11,
                day=20,
            ),
            story_points=8
        ),
    ]

    dvt = DeveloperVelocityTracker()

    for each in issues:
        dv = get_developer_velocity_from_issue(issue=each)
        dvt.add_velocity(dv)

    for each in Developer:
        print(dvt.get(each))

    print("AVERAGE: ", dvt.get_average_velocity())
