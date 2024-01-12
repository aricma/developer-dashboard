import dataclasses
from typing import List

import pytest

from business_logic.developer_velocity_tracker import DeveloperVelocityTracker
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.models.velocity_trackable_task import VelocityTrackableTask
from business_logic.test__track_developer_velocity import (
    DeveloperVelocityTrackerTestCase,
)


@dataclasses.dataclass
class TeamVelocityTrackerTestCase:
    message: str
    given: List[VelocityTrackableTask]
    expected: DeveloperVelocity


test_cases: List[TeamVelocityTrackerTestCase] = [
    TeamVelocityTrackerTestCase(
        message="Given no tasks, when call then no velocity is returned",
        given=[],
        expected={},
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished on the same day, when call then returns the velocity for that day",
        given=[
            VelocityTrackableTask(
                id="1",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 17),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={Date(2020, 5, 17).to_string(): 6},
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished on the next day, "
        "when call then returns half the story points as the velocity for both days",
        given=[
            VelocityTrackableTask(
                id="1",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 18),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={Date(2020, 5, 17).to_string(): 3, Date(2020, 5, 18).to_string(): 3},
    ),
    TeamVelocityTrackerTestCase(
        message="Given one task finished in three days, "
        "when call then returns one third of the story points as the velocity for each day",
        given=[
            VelocityTrackableTask(
                id="1",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 19),
                story_points=6,
                assignees=["Dave"],
            )
        ],
        expected={
            Date(2020, 5, 17).to_string(): 2,
            Date(2020, 5, 18).to_string(): 2,
            Date(2020, 5, 19).to_string(): 2,
        },
    ),
    TeamVelocityTrackerTestCase(
        message="Given multiple tasks finished on different days with no overlap, "
        "when called then returns the expected velocity for each day",
        given=[
            VelocityTrackableTask(
                id="1",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 19),
                story_points=6,
                assignees=["Dave"],
            ),
            VelocityTrackableTask(
                id="2",
                date_started=Date(2020, 5, 20),
                date_finished=Date(2020, 5, 21),
                story_points=4,
                assignees=["Steve"],
            ),
        ],
        expected={
            Date(2020, 5, 17).to_string(): 2,
            Date(2020, 5, 18).to_string(): 2,
            Date(2020, 5, 19).to_string(): 2,
            Date(2020, 5, 20).to_string(): 2,
            Date(2020, 5, 21).to_string(): 2,
        },
    ),
    TeamVelocityTrackerTestCase(
        message="Given multiple tasks finished on different days with overlap, "
        "when called then returns the expected velocity for each day with the overlap aggregated",
        given=[
            VelocityTrackableTask(
                id="1",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 19),
                story_points=6,
                assignees=["Dave"],
            ),
            VelocityTrackableTask(
                id="2",
                date_started=Date(2020, 5, 19),
                date_finished=Date(2020, 5, 21),
                story_points=6,
                assignees=["Steve"],
            ),
            VelocityTrackableTask(
                id="3",
                date_started=Date(2020, 5, 16),
                date_finished=Date(2020, 5, 17),
                story_points=6,
                assignees=["Paul", "Steve"],
            ),
            VelocityTrackableTask(
                id="3",
                date_started=Date(2020, 5, 17),
                date_finished=Date(2020, 5, 20),
                story_points=4,
                assignees=["Sarah", "Dave"],
            ),
        ],
        expected={
            Date(2020, 5, 16).to_string(): 3,
            Date(2020, 5, 17).to_string(): 6,
            Date(2020, 5, 18).to_string(): 3,
            Date(2020, 5, 19).to_string(): 5,
            Date(2020, 5, 20).to_string(): 3,
            Date(2020, 5, 21).to_string(): 2,
        },
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[each.message for each in test_cases]
)
def test__developer_velocity_tracker(
    test_case: DeveloperVelocityTrackerTestCase,
) -> None:
    velocity_tracker = DeveloperVelocityTracker()
    team_velocity = velocity_tracker.track_team_velocity(
        tasks=test_case.given,
    )
    assert team_velocity == test_case.expected
