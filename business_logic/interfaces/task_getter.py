from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class TaskGetter(ABC, Generic[T]):
    @abstractmethod
    def get_tasks(self) -> List[T]:
        ...
