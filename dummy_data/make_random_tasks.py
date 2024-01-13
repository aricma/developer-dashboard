import dataclasses
import json
import random
from dataclasses import asdict
from typing import List, Optional, TypeVar
from uuid import uuid4 as uuid
from dateutil.parser import parse as to_date
from datetime import timedelta as duration, datetime
import faker

NUMBER_OF_CREATED_TASKS = 8 * 5  # 8 weeks x 1 per work day
INITIAL_SUB_TASKS = 12
ABSOLUTE_START_DATE = str(datetime(year=2023, month=8, day=1))
ABSOLUTE_END_DATE = str(datetime.now())

fake = faker.Faker()

TaskID = str
Date = str
StoryPoints = float
DeveloperID = str


@dataclasses.dataclass
class Task:
    id: TaskID
    title: str
    description: str
    story_points: StoryPoints
    assignees: List[DeveloperID]
    sub_tasks: List["Task"]
    date_started: Date
    date_finished: Optional[Date] = None


@dataclasses.dataclass
class DummyTaskWithTitleAndDescription:
    title: str
    description: str


dummy_tasks_with_title_and_description = [
    DummyTaskWithTitleAndDescription(
        title="User Authentication Overhaul",
        description="Redesign the user authentication system to enhance security and implement two-factor authentication.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Database Schema Migration",
        description="Migrate the existing database schema to a new version with optimized tables for better performance.",
    ),
    DummyTaskWithTitleAndDescription(
        title="API Endpoint Creation for User Data",
        description="Develop new API endpoints to allow retrieval and update of user profile data.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Front-End Redesign of Dashboard",
        description="Overhaul the user dashboard interface to improve usability and incorporate a new design language.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Implement Caching for High-Traffic Services",
        description="Introduce caching mechanisms for high-traffic services to reduce load times and server stress.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Automated Testing for Checkout Process",
        description="Create a suite of automated tests to thoroughly test the e-commerce checkout process.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Bug Fix: Memory Leak in Data Processing Module",
        description="Investigate and fix the memory leak issue identified in the data processing module.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Mobile Responsiveness Enhancement",
        description="Improve the mobile responsiveness of the web application across various devices and screen sizes.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Integrate Third-Party Payment Gateway",
        description="Integrate a new third-party payment gateway to provide more payment options to users.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Implement Real-Time Notifications",
        description="Develop a real-time notification system for in-app alerts and messages.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Optimize Image Loading Times",
        description="Optimize the loading times for images in the application, including compression techniques and lazy loading.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Refactor User Settings Module",
        description="Refactor the user settings module for better code maintainability and future feature expansions.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Accessibility Compliance Audit",
        description="Conduct an audit of the application to ensure compliance with web accessibility standards.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Implement Feature Flag System",
        description="Develop a system for feature flags to enable easier management of feature rollouts and A/B testing.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Enhance Application Logging System",
        description="Enhance the current logging system to include more detailed application performance metrics.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Develop User Feedback Interface",
        description="Create an interface within the application for users to submit feedback and bug reports.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Cloud Storage Integration for User Files",
        description="Integrate a cloud storage solution for handling user file uploads and management.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Implement Chatbot for Customer Support",
        description="Develop an AI-driven chatbot to assist users with common queries and support issues.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Optimize Query Performance in Reporting Tool",
        description="Optimize the SQL queries used in the reporting tool to reduce execution times and improve efficiency.",
    ),
    DummyTaskWithTitleAndDescription(
        title="Create Developer Documentation Wiki",
        description="Set up a comprehensive wiki for developer documentation, including codebase walkthroughs and style guides.",
    ),
]


def make_fake_developer_name() -> str:
    return fake.random.choice(
        [
            "Adrian",
            "Elshafie",
            "Joshua",
            "Alexey",
            "Long",
        ]
    )


def make_fake_assignees() -> List[str]:
    number_of_assignees = random.choices(
        [1, 2, 3, 4, 5], [0.8, 0.15, 0.02, 0.015, 0.005], k=1
    )[0]
    return list(set([make_fake_developer_name() for _ in range(number_of_assignees)]))


def add_random_number_of_days_to_date(date: str, days: int) -> str:
    return str((to_date(date) + duration(days=days)).date())


def make_random_date_between(start_date: str, end_date: str) -> str:
    available_days = (to_date(end_date) - to_date(start_date)).days
    increase_by_days = random.randrange(available_days)
    return add_random_number_of_days_to_date(start_date, increase_by_days)


def make_uuid() -> str:
    return str(uuid())


def make_random_story_points() -> float:
    return random.choice([1, 2, 3, 5, 8])


T = TypeVar("T")


def make_optional_value(value: T) -> Optional[T]:
    return value if random.choice([True, False]) else None


def make_random_task_title_and_description() -> DummyTaskWithTitleAndDescription:
    return random.choice(dummy_tasks_with_title_and_description)


def aggregate_story_points_from_sub_tasks(sub_tasks: List[Task]) -> StoryPoints:
    aggregated_story_points = 0
    for task in sub_tasks:
        aggregated_story_points += task.story_points
    return aggregated_story_points


def make_random_task(number_of_sub_tasks: int):
    start_date = make_random_date_between(
        start_date=ABSOLUTE_START_DATE,
        end_date=ABSOLUTE_END_DATE,
    )
    end_date = make_random_date_between(
        start_date=start_date,
        end_date=ABSOLUTE_END_DATE,
    )
    dummy_task_title_and_description = make_random_task_title_and_description()
    sub_tasks = (
        [
            make_random_task(
                number_of_sub_tasks=(
                    int(random.randrange(number_of_sub_tasks - 2))
                    if number_of_sub_tasks > 2
                    else 0
                )
            )
            for _ in range(number_of_sub_tasks)
        ]
        if number_of_sub_tasks > 0
        else []
    )
    has_sub_tasks = len(sub_tasks) > 0
    story_points = (
        make_random_story_points()
        if not has_sub_tasks
        else aggregate_story_points_from_sub_tasks(sub_tasks)
    )
    return Task(
        id=make_uuid(),
        title=dummy_task_title_and_description.title,
        description=dummy_task_title_and_description.description,
        date_started=start_date,
        story_points=story_points,
        assignees=make_fake_assignees(),
        date_finished=make_optional_value(end_date) if len(sub_tasks) == 0 else None,
        sub_tasks=sub_tasks,
    )


def make_random_tasks():
    return {
        "tasks": [
            asdict(make_random_task(int(random.randrange(INITIAL_SUB_TASKS))))
            for _ in range(NUMBER_OF_CREATED_TASKS)
        ]
    }


if __name__ == "__main__":
    print(json.dumps(make_random_tasks(), indent=4, sort_keys=True))
