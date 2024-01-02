from pathlib import Path

API_URL_PREFIX = "/api/v1"
AUTHENTICATION_TOKEN_COOKIE_NAME = "developer-dashboard-authentication-token"
AUTHENTICATION_TOKEN_COOKIE_LIFE_TIME_IN_SECONDS = 6 * 60 * 60  # 6 hours
PATH_TO_HTML_FILES = Path(__file__).parent.parent / "static"
PATH_TO_ACCOUNTS_YML_FILE = Path(__file__).parent.parent / "accounts.yml"
PATH_TO_DEVELOPERS_JSON_FILE = Path(__file__).parent.parent / "developers.json"
PATH_TO_TASKS_JSON_FILE = Path(__file__).parent.parent / "tasks.json"
