import hashlib
from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import Generic, TypeVar, Callable, Union

from yaml import load, Loader


def print_api_title() -> None:
    server_title = """
 _____  ________      ________ _      ____  _____  ______ _____  
|  __ \|  ____\ \    / /  ____| |    / __ \|  __ \|  ____|  __ \ 
| |  | | |__   \ \  / /| |__  | |   | |  | | |__) | |__  | |__) |
| |  | |  __|   \ \/ / |  __| | |   | |  | |  ___/|  __| |  _  / 
| |__| | |____   \  /  | |____| |___| |__| | |    | |____| | \ \ 
|_____/|______|   \/   |______|______\____/|_|    |______|_|  \_\ 

                                                                                                
██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  
    """
    print(server_title)


T = TypeVar("T")


class ReaderInterface(ABC):
    @abstractmethod
    def unsafe_read(self) -> str:
        ...


class FileReader(ReaderInterface):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def unsafe_read(self) -> str:
        with open(self._file_path, "r") as reader:
            return reader.read()


class WriterInterface(ABC):
    @abstractmethod
    def unsafe_write(self, value: str) -> None:
        ...


class UpdaterInterface(ABC, Generic[T]):
    @abstractmethod
    def unsafe_update(self, record: T) -> None:
        ...


Update = Callable[[str], str]


class FileUpdater(UpdaterInterface):
    def __init__(
            self, reader: ReaderInterface, writer: WriterInterface, update: Update
    ):
        self._reader = reader
        self._writer = writer
        self._update = update

    def unsafe_update(self, record: T) -> None:
        file_content = self._reader.unsafe_read()
        updated_file_content = self._update(file_content)
        self._writer.unsafe_write(updated_file_content)


Date = str


def make_date(year: int, month: int, day: int) -> Date:
    return str(date(year, month, day))


def hash_string_value(value: str) -> str:
    return str(hashlib.md5(value.encode("utf-8")).hexdigest())


def read_yml_file_content(path: Union[Path, str]) -> dict:
    with open(path, "r") as reader:
        return load(reader.read(), Loader=Loader)
