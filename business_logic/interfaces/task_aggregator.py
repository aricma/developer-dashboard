from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class Aggregator(ABC, Generic[T]):
    @abstractmethod
    def aggregate(self, items: List[T]) -> T:
        ...
