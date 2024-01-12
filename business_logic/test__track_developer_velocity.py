import dataclasses
from datetime import datetime as date
from typing import List

import pytest

from business_logic.developer_velocity_tracker import Velocity, DeveloperVelocityTracker
from domain_models.task import FinishedTask


@dataclasses.dataclass
class DeveloperVelocityTrackerTestCase:
    message: str
    given: List[FinishedTask]
    tracked_developer: str
    expected: Velocity


test_cases: List[DeveloperVelocityTrackerTestCase] = [
    DeveloperVelocityTrackerTestCase(
        message="Given no tasks, when called no velocity can be calculated",
        given=[],
        tracked_developer="Dave",
        expected={},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given one task finished same day for tracked developer, "
        "when called story points of given task are returned as velocity",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Dave"],
            )
        ],
        tracked_developer="Dave",
        expected={str(date(2020, 5, 17)): 3},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given one task finished same day for different developer, "
        "when called no velocity is returned",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Steve"],
            )
        ],
        tracked_developer="Dave",
        expected={},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given two tasks finished by tracked and different developer, "
        "when called only expected velocity for tracked developer is returned",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Steve"],
            ),
            FinishedTask(
                id="2",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Dave"],
            ),
        ],
        tracked_developer="Dave",
        expected={str(date(2020, 5, 17)): 3},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given a task finished by two developers(including the tracked developer), "
        "when called a half of the story points is returned as velocity",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Steve", "Dave"],
            )
        ],
        tracked_developer="Dave",
        expected={str(date(2020, 5, 17)): 1.5},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given a task finished by three developers(including the tracked developer), "
        "when called a third of the story points is returned as velocity",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 17)),
                story_points=3,
                assignees=["Steve", "Dave", "Paul"],
            )
        ],
        tracked_developer="Dave",
        expected={str(date(2020, 5, 17)): 1},
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given a task finished the next day by the tracked developer, "
        "when called two velocities are returned splitting the story points between them",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 18)),
                story_points=4,
                assignees=["Dave"],
            )
        ],
        tracked_developer="Dave",
        expected={
            str(date(2020, 5, 17)): 2,
            str(date(2020, 5, 18)): 2,
        },
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given a task finished in three days by the tracked developer, "
        "when called three velocities are returned splitting the story points between them",
        given=[
            FinishedTask(
                id="1",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 19)),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        tracked_developer="Dave",
        expected={
            str(date(2020, 5, 17)): 2,
            str(date(2020, 5, 18)): 2,
            str(date(2020, 5, 19)): 2,
        },
    ),
    DeveloperVelocityTrackerTestCase(
        message="Given multiple tasks finished on different days by the tracked developer with overlap, "
        "when called returns the expected velocities",
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
                assignees=["Dave"],
            ),
            FinishedTask(
                id="3",
                date_started=str(date(2020, 5, 16)),
                date_finished=str(date(2020, 5, 17)),
                story_points=6,
                assignees=["Dave"],
            ),
            FinishedTask(
                id="3",
                date_started=str(date(2020, 5, 17)),
                date_finished=str(date(2020, 5, 20)),
                story_points=4,
                assignees=["Dave"],
            ),
        ],
        tracked_developer="Dave",
        expected={
            str(date(2020, 5, 16)): 3,
            str(date(2020, 5, 17)): 6,
            str(date(2020, 5, 18)): 3,
            str(date(2020, 5, 19)): 5,
            str(date(2020, 5, 20)): 3,
            str(date(2020, 5, 21)): 2,
        },
    ),
]

TRACKED_DEVELOPER = "Dave"


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[each.message for each in test_cases]
)
def test__developer_velocity_tracker(
    test_case: DeveloperVelocityTrackerTestCase,
) -> None:
    velocity_tracker = DeveloperVelocityTracker()
    developer_velocity = velocity_tracker.track_developer_velocity(
        tasks=test_case.given, tracked_developer=test_case.tracked_developer
    )
    assert developer_velocity == test_case.expected
