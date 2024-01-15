import dataclasses
import datetime
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Generic, TypeVar, Literal

from dateutil.parser import parse

from business_logic.interfaces.task_getter import TaskGetter, T

CacheEntryKey = str
TaskID = str
DateWithTime = str

K = TypeVar("K")
V = TypeVar("V")


@dataclasses.dataclass
class CacheEntryValue(Generic[V]):
    value: V
    expiration_date_and_time: DateWithTime


class Cache(ABC, Generic[K, V]):

    @abstractmethod
    def has(self, key: K) -> bool:
        ...

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        ...

    @abstractmethod
    def add(self, key: K, value: V) -> None:
        ...


class CacheUtils(Generic[V]):

    @staticmethod
    def make_cache_entry(value: V, cache_life_time_in_seconds: int) -> CacheEntryValue[V]:
        return CacheEntryValue(
            value=value,
            expiration_date_and_time=CacheUtils.make_expiration_date(cache_life_time_in_seconds)
        )

    @staticmethod
    def make_expiration_date(cache_life_time_in_seconds: int) -> str:
        now = datetime.datetime.now()
        duration_til_expiration = datetime.timedelta(
            seconds=cache_life_time_in_seconds
        )
        return str(now + duration_til_expiration)

    @staticmethod
    def cache_value_is_expired(value: CacheEntryValue[V]) -> bool:
        now = datetime.datetime.now()
        return now < parse(value.expiration_date_and_time)


class TaskCache(Cache[TaskID, T]):
    _cache: Dict[CacheEntryKey, CacheEntryValue[T]]

    def __init__(self, cache_utils: CacheUtils[T], cache_life_time_in_seconds: int):
        self._cache = {}
        self._utils = cache_utils
        self._cache_life_time_in_seconds = cache_life_time_in_seconds

    def has(self, key: TaskID) -> bool:
        cache_key = self._make_cache_key_for_task_id(key)
        return cache_key in self._cache.keys()

    def get(self, key: TaskID) -> Optional[T]:
        cache_key = self._make_cache_key_for_task_id(key)
        optional_cache_entry = self._cache.get(cache_key)
        if optional_cache_entry is not None and not self._utils.cache_value_is_expired(optional_cache_entry):
            return optional_cache_entry.value
        return None

    def add(self, key: TaskID, value: T) -> None:
        cache_entry = self._utils.make_cache_entry(
            value=value,
            cache_life_time_in_seconds=self._cache_life_time_in_seconds
        )
        cache_key = self._make_cache_key_for_task_id(key)
        self._cache[cache_key] = cache_entry

    @staticmethod
    def _make_cache_key_for_task_id(task_id: str) -> CacheEntryKey:
        return f"GET_TASK_BY_ID::WITH_TASK_ID::{task_id}"


class TasksCache(Cache[Literal["GET_TASKS"], List[T]]):
    _cached_tasks: Optional[CacheEntryValue[List[T]]]

    def __init__(self, cache_utils: CacheUtils[List[T]], cache_life_time_in_seconds: int):
        self._cached_tasks = None
        self._utils = cache_utils
        self._cache_life_time_in_seconds = cache_life_time_in_seconds

    def has(self, key: Literal["GET_TASKS"]) -> bool:
        return self._cached_tasks is not None

    def get(self, key: Literal["GET_TASKS"]) -> Optional[List[T]]:
        optional_cache_entry = self._cached_tasks
        if optional_cache_entry is not None and not self._utils.cache_value_is_expired(optional_cache_entry):
            return optional_cache_entry.value
        return None

    def add(self, key: Literal["GET_TASKS"], value: List[T]) -> None:
        self._cached_tasks = self._utils.make_cache_entry(
            value=value,
            cache_life_time_in_seconds=self._cache_life_time_in_seconds
        )


class CachingTaskGetter(TaskGetter[T]):

    def __init__(
            self,
            task_getter: TaskGetter[T],
            task_cache: Cache[TaskID, T],
            tasks_cache: Cache[Literal["GET_TASKS"], List[T]],
            cache_life_time_in_seconds: int
    ):
        self._task_getter = task_getter
        self._cache_life_time_in_seconds = cache_life_time_in_seconds
        self._tasks_cache = tasks_cache
        self._task_cache = task_cache

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
        self._tasks_cache.add(
            key="GET_TASKS",
            value=tasks,
        )

    def _get_tasks_from_cache(self) -> Optional[List[T]]:
        return self._tasks_cache.get("GET_TASKS")

    def _add_task_for_id_to_cache(self, task_id: TaskID, task: T) -> None:
        self._task_cache.add(
            key=task_id,
            value=task,
        )

    def _get_task_for_id_from_cache(self, task_id: str) -> Optional[T]:
        return self._task_cache.get(key=task_id)
