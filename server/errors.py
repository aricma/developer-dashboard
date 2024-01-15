from http.client import HTTPException


class MissingAuthenticationTokenCookie(HTTPException):
    def __init__(self) -> None:
        super().__init__("Missing Authentication Cookie")


class MissingAccountForAuthenticationToken(HTTPException):
    def __init__(self) -> None:
        super().__init__("Missing account for given authentication token")
