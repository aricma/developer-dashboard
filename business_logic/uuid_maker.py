from uuid import uuid4

from business_logic.interfaces.maker import Maker, T


class UUIDMaker(Maker[str]):

    def make(self) -> T:
        return str(uuid4())
