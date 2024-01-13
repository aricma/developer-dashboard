from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Decimator(ABC, Generic[T]):
    @abstractmethod
    def decimate(self, value: T) -> T:
        ...
