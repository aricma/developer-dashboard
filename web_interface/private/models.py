from typing import Union, Literal

Alignment = Union[
    Literal["start"],
    Literal["center"],
    Literal["end"],
    Literal["between"],
    Literal["around"],
    Literal["evenly"],
]

ChartType = Union[
    Literal["velocity"],
    Literal["burn-down"],
]
