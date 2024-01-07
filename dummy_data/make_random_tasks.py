import json
import random
from dataclasses import asdict
from typing import List
from uuid import uuid4 as uuid
from dateutil.parser import parse as to_date
from datetime import timedelta as duration, datetime
import faker

from domain_models.task import FinishedTask

NUMBER_OF_CREATED_TASKS = 8 * 5  # 8 weeks x 1 per work day
ABSOLUTE_START_DATE = str(datetime(year=2023, month=8, day=1))
ABSOLUTE_END_DATE = str(datetime.now())

fake = faker.Faker()


def make_fake_developer_name() -> str:
    return fake.random.choice([
        "Adrian",
        "Elshafie",
        "Joshua",
        "Alexey",
        "Long",
    ])


def make_fake_assignees() -> List[str]:
    number_of_assignees = random.choices([1, 2, 3, 4, 5], [.8, .15, .02, .015, .005], k=1)[0]
    return list(set([make_fake_developer_name() for _ in range(number_of_assignees)]))


def add_random_number_of_days_to_date(date: str, days: int) -> str:
    return str(to_date(date) + duration(days=days))


def make_random_date_between(start_date: str, end_date: str) -> str:
    available_days = (to_date(end_date) - to_date(start_date)).days
    increase_by_days = random.randrange(available_days)
    return add_random_number_of_days_to_date(start_date, increase_by_days)


def make_uuid() -> str:
    return str(uuid())


def make_random_story_points() -> float:
    return random.randrange(128)


def make_random_task():
    start_date = make_random_date_between(
        start_date=ABSOLUTE_START_DATE,
        end_date=ABSOLUTE_END_DATE,
    )
    end_date = make_random_date_between(
        start_date=start_date,
        end_date=ABSOLUTE_END_DATE,
    )
    return FinishedTask(
        id=make_uuid(),
        date_started=start_date,
        date_finished=end_date,
        story_points=make_random_story_points(),
        assignees=make_fake_assignees(),
    )


def make_random_tasks():
    data = {
        "tasks": [
            asdict(make_random_task())
            for _ in range(NUMBER_OF_CREATED_TASKS)
        ]
    }
    print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == '__main__':
    make_random_tasks()
