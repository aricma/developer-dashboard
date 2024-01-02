from typing import List, Dict

from pydantic import BaseModel

from business_logic.models import Permissions


class _VelocityDatapoint(BaseModel):
    date: str
    velocity_as_story_points_per_day: int


class _Developer(BaseModel):
    id: str
    name: str
    velocity: List[_VelocityDatapoint]


class DevelopersDataFile(BaseModel):
    developers: List[_Developer]


class _BurnDownDataPoint(BaseModel):
    date: str
    remaining_story_points: int


class Task(BaseModel):
    id: str
    title: str
    # description: str
    # responsible: str
    burn_down_data: List[_BurnDownDataPoint]


class TaskDataFile(BaseModel):
    tasks: List[Task]


_AccountID = str


class Account(BaseModel):
    id: _AccountID
    name: str
    email: str
    hashed_password: str
    permissions: Permissions


class AccountInfo(BaseModel):
    name: str
    email: str
    permissions: List[str]


class Configuration(BaseModel):
    accounts: Dict[_AccountID, Account]
