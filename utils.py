from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable


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

    def __init__(self, reader: ReaderInterface, writer: WriterInterface, update: Update):
        self._reader = reader
        self._writer = writer
        self._update = update

    def unsafe_update(self, record: T) -> None:
        file_content = self._reader.unsafe_read()
        updated_file_content = self._update(file_content)
        self._writer.unsafe_write(updated_file_content)
