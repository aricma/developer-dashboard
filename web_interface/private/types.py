from typing import Dict, Union, List

HTMLElement = Union[List["HTMLElement"], str, None]
Props = Dict[str, HTMLElement]


class SkipMissingProps(Props):

    def __missing__(self, _: str) -> str:
        return ""



class KeepMissingProps(Props):

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"
