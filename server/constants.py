from pathlib import Path

from server import envorinment


class Time:
    @staticmethod
    def hours(value: int) -> int:
        return value * 60 * 60

    @staticmethod
    def minutes(value: int) -> int:
        return value * 60

    @staticmethod
    def seconds(value: int) -> int:
        return value


API_URL_PREFIX = "/api/v1"
AUTHENTICATION_TOKEN_COOKIE_NAME = "developer-dashboard-authentication-token"
AUTHENTICATION_TOKEN_COOKIE_LIFE_TIME_IN_SECONDS = Time.hours(3)
PATH_TO_STATIC_FILES = Path(__file__).parent.parent / envorinment.STATIC_FOLDER_NAME
PATH_TO_HTML_FILES = PATH_TO_STATIC_FILES
PATH_TO_ACCOUNTS_YML_FILE = Path(__file__).parent.parent / "accounts.yml"
