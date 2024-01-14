import dataclasses
import datetime
from typing import List, Optional, Any, Dict

from dateutil.parser import parse

from business_logic.interfaces.task_getter import TaskGetter, T

CacheEntryKey = str
TaskID = str
DateWithTime = str


@dataclasses.dataclass
class CacheEntryValue:
    value: Any
    expiration_date_and_time: DateWithTime


class CachingTaskGetter(TaskGetter[T]):
    _cache: Dict[CacheEntryKey, CacheEntryValue]

    def __init__(self, task_getter: TaskGetter[T], cache_life_time_in_seconds: int):
        self._task_getter = task_getter
        self._cache_life_time_in_seconds = cache_life_time_in_seconds
        self._cache = {}

    def get_task_by_id(self, task_id: str) -> Optional[T]:
        cached_task = self._get_task_for_id_from_cache(task_id)
        if cached_task is not None:
            return cached_task
        new_task = self._task_getter.get_task_by_id(task_id)
        if new_task is None:
            return None
        self._add_task_for_id_to_cache(task_id=task_id, task=new_task)
        return new_task

    def get_tasks(self) -> List[T]:
        cached_tasks = self._get_tasks_from_cache()
        if cached_tasks is not None:
            return cached_tasks
        new_tasks = self._task_getter.get_tasks()
        self._add_tasks_to_cache(tasks=new_tasks)
        return new_tasks

    def _add_tasks_to_cache(self, tasks: List[T]) -> None:
        self._add_entry_to_cache(
            key=self._make_cache_key_for_all_tasks(),
            value=CacheEntryValue(
                value=tasks,
                expiration_date_and_time=self._make_expiration_date(),
            ),
        )

    def _get_tasks_from_cache(self) -> Optional[List[T]]:
        cached_value = self._check_cache_for_entry(
            key=self._make_cache_key_for_all_tasks()
        )
        if cached_value is None:
            return None
        return cached_value.value

    def _add_task_for_id_to_cache(self, task_id: TaskID, task: T) -> None:
        self._add_entry_to_cache(
            key=self._make_cache_key_for_task_id(task_id=task_id),
            value=CacheEntryValue(
                value=task,
                expiration_date_and_time=self._make_expiration_date(),
            ),
        )

    def _get_task_for_id_from_cache(self, task_id: str) -> Optional[T]:
        cached_value = self._check_cache_for_entry(
            key=self._make_cache_key_for_task_id(task_id=task_id)
        )
        if cached_value is None:
            return None
        return cached_value.value

    def _check_cache_for_entry(self, key: CacheEntryKey) -> Optional[CacheEntryValue]:
        optional_cache_value = self._get_entry_from_cache(key)
        if optional_cache_value is None:
            return None
        if self._cache_value_is_expired(optional_cache_value):
            return None
        return optional_cache_value

    def _add_entry_to_cache(self, key: CacheEntryKey, value: CacheEntryValue) -> None:
        self._cache[key] = value

    def _get_entry_from_cache(self, key: CacheEntryKey) -> Optional[CacheEntryValue]:
        return self._cache.get(key)

    def _make_expiration_date(self) -> str:
        now = self._today = datetime.datetime.now()
        duration_til_expiration = datetime.timedelta(
            seconds=self._cache_life_time_in_seconds
        )
        return str(now + duration_til_expiration)

    def _cache_value_is_expired(self, value: CacheEntryValue) -> bool:
        now = self._today = datetime.datetime.now()
        return now < parse(value.expiration_date_and_time)

    @staticmethod
    def _make_cache_key_for_task_id(task_id: str) -> CacheEntryKey:
        return f"GET_TASK_BY_ID::WITH_TASK_ID::{task_id}"

    @staticmethod
    def _make_cache_key_for_all_tasks() -> CacheEntryKey:
        return "GET_TASKS"
