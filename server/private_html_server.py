from http.client import HTTPException
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, FileResponse, RedirectResponse

from business_logic._business_logic import BusinessLogic
from business_logic.marshalls import Account
from server import constants
from server.authentication_utils import create_authentication_token_cookie_value
from web_interface.pages.make_dashboard_burn_down_page import make_dashboard_burn_down_page
from web_interface.pages.make_dashboard_overview_page import make_dashboard_overview_page
from web_interface.pages.make_dashboard_velocity_page import make_dashboard_velocity_page
from web_interface.pages.make_error_page import make_error_page

private_app = FastAPI(
    title="Developer Dashboard Web Server(Private)",
)


@private_app.exception_handler(HTTPException)
async def server_error_exception_handler(_, exc: HTTPException):
    if isinstance(exc, MissingAuthenticationTokenCookie):
        return redirect_to_login_page()
    else:
        error_message = limit_string(str(exc), character_limit=500)
        return HTMLResponse(
            content=make_error_page(
                error_code="500",
                message=f"There was an unknown error raised by the server: \"{error_message}\". "
                        "Please create a ticket at https://github.com/aricma/developer-dashboard."
            )
        )


business_logic = BusinessLogic(
    path_to_accounts_yml_file=str(constants.PATH_TO_ACCOUNTS_YML_FILE),
    path_to_developers_json_file=str(constants.PATH_TO_DEVELOPERS_JSON_FILE),
    path_to_tasks_json_file=str(constants.PATH_TO_TASKS_JSON_FILE),
)


@private_app.middleware("http")
async def check_for_authentication_cookie(request: Request, call_next):
    optional_authentication_token = request.cookies.get(constants.AUTHENTICATION_TOKEN_COOKIE_NAME)
    if optional_authentication_token is not None and authentication_token_is_valid(token=optional_authentication_token):
        response = await call_next(request)
        return refresh_authentication_token_cookie_value(
            response=response,
            old_authentication_token=optional_authentication_token
        )
    return redirect_to_login_page()


@private_app.get("/dashboard/overview")
async def get_dashboard_overview_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_overview_page(
            user_name=account.name,
            # burn_down_warnings=[
            #     Alert(
            #         title="Rising Task Burn Down Metric",
            #         description="Attention you have a rising Task Burn Down Metric. "
            #                     "Make sure this happened because of changes in scope."
            #     )
            # ]
        )
    )


@private_app.get("/dashboard/velocity")
async def get_dashboard_velocity_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_velocity_page(
            user_name=account.name,
            last_two_weeks_velocity_chart_data_file_name=business_logic.get_velocity_data_file_name_for_developer(
                account=account,
                time_in_weeks=2,
            ),
            last_four_weeks_velocity_chart_data_file_name=business_logic.get_velocity_data_file_name_for_developer(
                account=account,
                time_in_weeks=4,
            ),
            last_eight_weeks_velocity_chart_data_file_name=business_logic.get_velocity_data_file_name_for_developer(
                account=account,
                time_in_weeks=8,
            ),
        )
    )


@private_app.get("/dashboard/burn-down")
async def get_dashboard_burn_down_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    # data = business_logic.get_task_burn_down_data_for_account(account=account)

    return HTMLResponse(
        content=make_dashboard_burn_down_page(
            user_name=account.name,
            data_file_name="./foobar-task-burn-down-metric.json"
        )
    )


@private_app.get("/{file_path}")
async def serve_all_files_that_requested_by_html_files(file_path: Optional[str] = None):
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(constants.PATH_TO_HTML_FILES / resolved_file_path)


def authentication_token_is_valid(token: Optional[str] = None) -> bool:
    return token is not None  # ⚠️ TODO: not implemented


def redirect_to_login_page() -> RedirectResponse:
    return RedirectResponse(
        url="/sign-in",
        status_code=307,
    )


def redirect_to_logout_page() -> RedirectResponse:
    return RedirectResponse(
        url="/sign-out",
        status_code=307,
    )


class MissingAuthenticationTokenCookie(HTTPException):

    def __init__(self):
        super().__init__("Missing Authentication Cookie")


class MissingAccountForAuthenticationToken(HTTPException):

    def __init__(self):
        super().__init__("Missing account for given authentication token")


def refresh_authentication_token_cookie_value(response: Response, old_authentication_token: str) -> Response:
    account: Optional[Account] = business_logic.get_account_for_jwt(old_authentication_token)
    if not account:
        raise MissingAccountForAuthenticationToken()
    authentication_token = business_logic.unsafe_create_authentication_token(account)
    response.headers["Set-Cookie"] = create_authentication_token_cookie_value(authentication_token)
    return response


def unsafe_get_account_from_authentication_token_cookie(request: Request) -> Account:
    optional_authentication_token = request.cookies.get(constants.AUTHENTICATION_TOKEN_COOKIE_NAME)
    if optional_authentication_token:
        account = business_logic.get_account_for_jwt(optional_authentication_token)
        if account:
            return account
        raise MissingAccountForAuthenticationToken()
    raise MissingAuthenticationTokenCookie()


