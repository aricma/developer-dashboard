from http.client import HTTPException

from business_logic.marshalls import Account


class ServerError(HTTPException):
    """
    This class is added to fast apis exception handlers
    """

    def __init__(self, message: str):
        super().__init__(f"ServerError: {message}")


class AccountAlreadyExists(KeyError, ServerError):

    def __init__(self, account: Account):
        super().__init__(
            f"Account with "
            f"name: \"{account.name}\", "
            f"email: \"{account.email}\", "
            f"and given password already exists."
        )


class InvalidCredentials(ValueError, ServerError):

    def __init__(self):
        super().__init__("Given email and password are invalid.")


class DummyDataNotFoundError(FileNotFoundError, ServerError):

    def __init__(self):
        super().__init__("Velocity Dummy Data is not created.")
