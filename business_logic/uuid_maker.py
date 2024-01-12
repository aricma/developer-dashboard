from uuid import uuid4

from business_logic.interfaces.maker import Maker


class UUIDMaker(Maker[str]):
    def make(self) -> str:
        return str(uuid4())
