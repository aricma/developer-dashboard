from typing import Set, Union, Literal


Permissions = Set[Union[Literal["READ_ALL", "READ_MINE", "READ_AND_WRITE_ALL"]]]
