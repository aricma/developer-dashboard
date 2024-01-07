import dataclasses
from typing import List
from datetime import datetime as date

import pytest

from business_logic.developer_velocity_tracker import Velocity, DeveloperVelocityTracker
from domain_models.task import FinishedTask
from business_logic.test__track_developer_velocity import DeveloperVelocityTrackerTestCase


@dataclasses.dataclass
class TeamVelocityTrackerTestCase:
    message: str
    given: List[FinishedTask]
    expected: Velocity


test_cases: List[TeamVelocityTrackerTestCase] = [
    TeamVelocityTrackerTestCase(
        message="Given no tasks, when call then no velocity is returned",
        given=[],
        expected={}
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished on the same day, when call then returns the velocity for that day",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={
            str(date(2020, 5, 17)): 6
        }
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished on the next day, "
                "when call then returns half the story points as the velocity for both days",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 18)),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={
            str(date(2020, 5, 17)): 3,
            str(date(2020, 5, 18)): 3
        }
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished in three days, "
                "when call then returns one third of the story points as the velocity for each day",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 19)),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={
            str(date(2020, 5, 17)): 2,
            str(date(2020, 5, 18)): 2,
            str(date(2020, 5, 19)): 2,
        }
    ),
    TeamVelocityTrackerTestCase(
        message="Given multiple tasks finished on different days with no overlap, "
                "when called then returns the expected velocity for each day",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 19)),
                story_points=6,
                assignees=["Dave"],
            ),
            FinishedTask(
                id="2",
                date_started=str(date(2020, 5, 20)),
                date_finished=str(date(2020, 5, 21)),
                story_points=4,
                assignees=["Steve"],
            )
        ],
        expected={
            str(date(2020, 5, 17)): 2,
            str(date(2020, 5, 18)): 2,
            str(date(2020, 5, 19)): 2,
            str(date(2020, 5, 20)): 2,
            str(date(2020, 5, 21)): 2,
        }
    ),
    TeamVelocityTrackerTestCase(
        message="Given multiple tasks finished on different days with overlap, "
                "when called then returns the expected velocity for each day with the overlap aggregated",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 19)),
                story_points=6,
                assignees=["Dave"],
            ),
            FinishedTask(
                id="2",
                date_started=str(date(2020, 5, 19)),
                date_finished=str(date(2020, 5, 21)),
                story_points=6,
                assignees=["Steve"],
            ),
            FinishedTask(
                id="3",
                date_started=str(date(2020, 5, 16)),
                date_finished=str(date(2020, 5, 17)),
                story_points=6,
                assignees=["Paul", "Steve"],
            ),
            FinishedTask(
                id="3",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 20)),
                story_points=4,
                assignees=["Sarah", "Dave"],
            )
        ],
        expected={
            str(date(2020, 5, 16)): 3,
            str(date(2020, 5, 17)): 6,
            str(date(2020, 5, 18)): 3,
            str(date(2020, 5, 19)): 5,
            str(date(2020, 5, 20)): 3,
            str(date(2020, 5, 21)): 2,
        }
    ),
]


@pytest.mark.parametrize("test_case", test_cases, ids=[each.message for each in test_cases])
def test__developer_velocity_tracker(test_case: DeveloperVelocityTrackerTestCase) -> None:
    velocity_tracker = DeveloperVelocityTracker()
    team_velocity = velocity_tracker.track_team_velocity(
        tasks=test_case.given,
    )
    assert team_velocity == test_case.expected
