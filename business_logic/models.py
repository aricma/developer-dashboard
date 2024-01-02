from typing import Set, Union, Literal

from pydantic import BaseModel

Permissions = Set[Union[Literal["READ_ALL", "READ_MINE", "READ_AND_WRITE_ALL"]]]
