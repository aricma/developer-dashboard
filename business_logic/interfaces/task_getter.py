from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Optional

T = TypeVar("T")


class TaskGetter(ABC, Generic[T]):
    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Optional[T]:
        ...

    @abstractmethod
    def get_tasks(self) -> List[T]:
        ...
