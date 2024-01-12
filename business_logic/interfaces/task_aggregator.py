from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class TaskAggregator(ABC, Generic[T]):
    @abstractmethod
    def aggregate(self, tasks: List[T]) -> T:
        ...
