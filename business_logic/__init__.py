import dataclasses
import datetime
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Union
from dateutil.parser import parse as to_date

import jwt
from pydantic import BaseModel
from yaml import dump, Dumper, load, Loader

from business_logic.developer_velocity_tracker import DeveloperVelocityTracker, Velocity
from business_logic.errors import AccountAlreadyExistsError, InvalidCredentialsError, DummyDataNotFoundError
from business_logic.marshalls import Account, Configuration, _Developer, DevelopersDataFile, Task, TaskDataFile, \
    AccountInfo
from domain_models.task import FinishedTask
from server import constants
from server.constants import PATH_TO_STATIC_FILES

JWT_ALGORITHM = "HS256"
JWT_KEY = "SECRET"

Date = str
StoryPoints = float


class DummyDataTask(BaseModel):
    id: str
    date_finished: str
    date_started: str
    story_points: float
    assignees: List[str]


DummyDataTasks = List[DummyDataTask]


class DummyDatafile(BaseModel):
    tasks: DummyDataTasks


@dataclasses.dataclass
class VelocityChartDataPoint:
    x: Date
    y: StoryPoints


VelocityChartDataPoints = List[VelocityChartDataPoint]


@dataclasses.dataclass
class VelocityChartData:
    developer_velocity: VelocityChartDataPoints
    average_developer_velocity: VelocityChartDataPoints


@dataclasses.dataclass
class VelocityChartDataFile:
    data_points: VelocityChartData


class BusinessLogic:

    def __init__(self,
                 path_to_accounts_yml_file: str,
                 path_to_developers_json_file: str,
                 path_to_tasks_json_file: str,
                 ):
        self._path_to_accounts_yml_file = path_to_accounts_yml_file
        self._path_to_developers_json_file = path_to_developers_json_file
        self._path_to_tasks_json_file = path_to_tasks_json_file
        self._velocity_tracker = DeveloperVelocityTracker()

    def get_velocity_data_file_name_for_developer(self, account: Account, time_in_weeks: int) -> str:
        # TODO: this function does 2 things
        data = self._get_velocity_data_for_developer(account, time_in_weeks=time_in_weeks)
        formatted_data = self._pretty_format_json(dataclasses.asdict(data))
        file_name = self._make_velocity_data_file_name_for_developer(
            developer_id=account.id,
            data_finger_print=self._hash(formatted_data)
        )
        if not self._static_file_does_exist(file_name):
            self._write_velocity_data_to_file(file_name, formatted_data)
        return file_name

    def _static_file_does_exist(self, file_name: str) -> bool:
        return self._file_does_exist(PATH_TO_STATIC_FILES / file_name)

    @staticmethod
    def _file_does_exist(path: str) -> bool:
        return Path(path).exists() and Path(path).is_file()

    @staticmethod
    def _make_velocity_data_file_name_for_developer(developer_id: str, data_finger_print: str) -> str:
        return f"{developer_id}-velocity-data-{data_finger_print}.json"

    @staticmethod
    def _pretty_format_json(value: Union[dict, list]) -> str:
        return json.dumps(value, indent=4, sort_keys=True)

    def _write_velocity_data_to_file(self, file_name: str, data: str) -> None:
        self._write_data_to_file(
            path=str(PATH_TO_STATIC_FILES / file_name),
            data=data
        )

    @staticmethod
    def _write_data_to_file(path: str, data: str) -> None:
        with open(path, "w") as writer:
            writer.write(data)

    def _get_velocity_data_for_developer(self, account: Account, time_in_weeks: int) -> VelocityChartDataFile:
        tracking_start_date = str(datetime.date.today() - datetime.timedelta(weeks=time_in_weeks))
        dummy_data_tasks = self._get_dummy_data_tasks()
        trackable_finished_tasks = self._dummy_data_to_trackable_data(
            self._filter_tasks_before_given_start_date(
                tasks=dummy_data_tasks.tasks,
                start_date=tracking_start_date,
            )
        )
        developer_velocity_data = self._velocity_tracker.track_developer_velocity(
            tasks=trackable_finished_tasks,
            tracked_developer=account.name,
        )
        average_developer_velocity_data = self._velocity_tracker.track_average_developer_velocity(
            tasks=trackable_finished_tasks
        )
        return VelocityChartDataFile(
            data_points=VelocityChartData(
                developer_velocity=self._sort_data_points_by_date(
                    data_points=self._velocity_to_chart_data_points(
                        velocity=self._filter_velocity_before_given_start_date(
                            velocity=developer_velocity_data,
                            start_date=tracking_start_date,
                        )
                    ),
                ),
                average_developer_velocity=self._sort_data_points_by_date(
                    data_points=self._velocity_to_chart_data_points(
                        velocity=self._filter_velocity_before_given_start_date(
                            velocity=average_developer_velocity_data,
                            start_date=tracking_start_date,
                        )
                    ),
                ),
            )
        )

    @staticmethod
    def _filter_tasks_before_given_start_date(tasks: DummyDataTasks, start_date: str) -> DummyDataTasks:
        return [
            task
            for task in tasks
            if to_date(task.date_finished) >= to_date(start_date)
        ]

    @staticmethod
    def _dummy_data_to_trackable_data(dummy_data: DummyDataTasks) -> List[FinishedTask]:
        return [
            FinishedTask(
                id=dummy_data_task.id,
                date_started=dummy_data_task.date_started,
                date_finished=dummy_data_task.date_finished,
                story_points=dummy_data_task.story_points,
                assignees=dummy_data_task.assignees,
            )
            for dummy_data_task in dummy_data
        ]

    @staticmethod
    def _filter_velocity_before_given_start_date(velocity: Velocity, start_date: str) -> Velocity:
        return {
            date: story_points
            for date, story_points in velocity.items()
            if to_date(date) >= to_date(start_date)
        }

    @staticmethod
    def _sort_data_points_by_date(data_points: VelocityChartDataPoints) -> VelocityChartDataPoints:
        return sorted(data_points, key=lambda data_point: data_point.x)

    @staticmethod
    def _velocity_to_chart_data_points(velocity: Velocity) -> VelocityChartDataPoints:
        return [
            VelocityChartDataPoint(
                x=date,
                y=story_points,
            )
            for date, story_points in velocity.items()
        ]

    def _get_dummy_data_tasks(self) -> DummyDatafile:
        file_path_to_dummy_data = constants.PATH_TO_VELOCITY_DUMMY_DATA
        if file_path_to_dummy_data.exists() and file_path_to_dummy_data.is_file():
            return DummyDatafile(**self._read_json_file_content(file_path_to_dummy_data))
        raise DummyDataNotFoundError()

    def get_task_burn_down_data_for_account(self, account: Account) -> dict:
        ...

    def get_account_for_jwt(self, authentication_token: str) -> Account:
        account_info = AccountInfo(
            **jwt.decode(
                jwt=authentication_token,
                key=JWT_KEY,
                algorithms=[JWT_ALGORITHM]
            )
        )
        return self.get_account_for_email(email=account_info.email)

    def unsafe_register_account(self, name: str, email: str, password: str) -> Account:
        account = self._create_account(name, email, password)
        self._unsafe_store_accounts(accounts=[account])
        return account

    def _unsafe_store_accounts(self, accounts: List[Account]) -> None:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = self._read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{
                "accounts": {}
            })

        for account in accounts:
            if account.id in configuration.accounts:
                raise AccountAlreadyExistsError(account)
            configuration.accounts[account.id] = account

        new_file_content = dump(configuration.model_dump(), Dumper=Dumper)

        with open(file_path, "w") as writer:
            writer.write(new_file_content)

    def unsafe_read_developer_data(self) -> List[_Developer]:
        file_path = Path(self._path_to_developers_json_file)
        file_content = self._read_json_file_content(file_path)

        return DevelopersDataFile(**file_content).developers

    def unsafe_read_task_data(self) -> List[Task]:
        file_path = Path(self._path_to_tasks_json_file)
        file_content = self._read_json_file_content(file_path)

        return TaskDataFile(**file_content).tasks

    def _create_account(self, name: str, email: str, password: str) -> Account:
        return Account(
            id=self._hash(self._create_account_signature(name, email, password)),
            name=name,
            email=email,
            hashed_password=self._hash_password(password),
            permissions={"READ_MINE"}
        )

    def unsafe_login(self, email: str, password: str) -> str:
        account = self.get_account_for_email(email=email)

        if not account:
            raise InvalidCredentialsError()

        password_is_valid = self.validate_password_against_account(
            account=account,
            password=password
        )

        if not password_is_valid:
            raise InvalidCredentialsError()

        return self.unsafe_create_authentication_token(account)

    @staticmethod
    def unsafe_create_authentication_token(account: Account) -> str:
        return jwt.encode(
            payload={
                "name": account.name,
                "email": account.email,
                "permissions": list(account.permissions)
            },
            key=JWT_KEY,
            algorithm=JWT_ALGORITHM
        )

    def get_account_for_email(self, email: str) -> Optional[Account]:
        for account in self._get_accounts_from_file().values():
            if account.email == email:
                return account
        return None

    def validate_password_against_account(self, account: Account, password: str) -> bool:
        return account.hashed_password == self._hash_password(password)

    def _get_accounts_from_file(self) -> Dict[str, Account]:
        file_path = Path(self._path_to_accounts_yml_file)
        if file_path.is_file():
            file_content = self._read_yml_file_content(file_path)
            configuration = Configuration(**file_content)
        else:
            configuration = Configuration(**{
                "accounts": {}
            })

        return configuration.accounts

    def _hash_password(self, password: str) -> str:
        return self._hash(password)

    @staticmethod
    def _read_json_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return json.loads(reader.read())

    @staticmethod
    def _read_yml_file_content(value: Path) -> dict:
        with open(value, "r") as reader:
            return load(reader.read(), Loader=Loader)

    @staticmethod
    def _create_account_signature(name: str, email: str, password: str) -> str:
        return f"{name}::{email}::{password}"

    @staticmethod
    def _hash(value: str) -> str:
        return str(hashlib.md5(value.encode("utf-8")).hexdigest())
