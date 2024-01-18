from typing import Dict, Union, List, TypeVar

HTMLElement = Union[List["HTMLElement"], str, None]
Props = Dict[str, HTMLElement]

K = TypeVar("K")
V = TypeVar("V")


class SkipMissingDict(Dict[K, V]):

    def __missing__(self, _: K) -> str:
        return ""


class KeepMissingDict(Dict[K, V]):

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"
