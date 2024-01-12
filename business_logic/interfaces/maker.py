from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Maker(ABC, Generic[T]):
    @abstractmethod
    def make(self) -> T:
        ...
