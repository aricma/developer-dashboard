from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse

from business_logic.business_logic import BusinessLogic
from business_logic.errors import ServerError
from business_logic.marshalls import Account
from server import constants
from web_interface.private.pages.make_dashboard_burn_down_page import make_dashboard_burn_down_page
from web_interface.private.pages.make_dashboard_overview_page import make_dashboard_overview_page
from web_interface.private.pages.make_dashboard_velocity_page import make_dashboard_velocity_page
from web_interface.private.pages.make_error_page import make_error_page

private_app = FastAPI(
    title="Developer Dashboard Web Server(Private)",
)


@private_app.exception_handler(ServerError)
async def server_error_exception_handler(_, exc: BaseException):
    if isinstance(exc, MissingAuthenticationTokenCookie):
        return redirect_to_login_page()
    else:
        return HTMLResponse(
            content=make_error_page(
                error_code="500",
                message="There was an unknown error raised by the server: \"{str(exc)}\". "
                        "Please create a ticket at https://github.com/aricma/developer-dashboard."
            )
        )


business_logic = BusinessLogic(
    path_to_accounts_yml_file=constants.PATH_TO_ACCOUNTS_YML_FILE,
    path_to_developers_json_file=constants.PATH_TO_DEVELOPERS_JSON_FILE,
    path_to_tasks_json_file=constants.PATH_TO_TASKS_JSON_FILE,
)


@private_app.middleware("http")
async def check_for_authentication_cookie(request: Request, call_next):
    optional_authentication_token = request.cookies.get(constants.AUTHENTICATION_TOKEN_COOKIE_NAME)
    if authentication_token_is_valid(token=optional_authentication_token):
        return await call_next(request)
    return redirect_to_login_page()


@private_app.get("/dashboard/overview")
async def get_dashboard_overview_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_overview_page(
            user_name=account.name
        )
    )


@private_app.get("/dashboard/velocity")
async def get_dashboard_velocity_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_velocity_page(
            user_name=account.name
        )
    )


@private_app.get("/dashboard/burn-down")
async def get_dashboard_burn_down_page(request: Request):
    account = unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_burn_down_page(
            user_name=account.name
        )
    )


@private_app.get("/{file_path}")
async def serve_all_files_that_requested_by_html_files(file_path: str = None):
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(constants.PATH_TO_HTML_FILES / resolved_file_path)


def authentication_token_is_valid(token: str = None) -> bool:
    return token is not None  # ⚠️ not implemented


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


class MissingAuthenticationTokenCookie(KeyError):

    def __init__(self):
        super().__init__("Missing Authentication Cookie")


def unsafe_get_account_from_authentication_token_cookie(request: Request) -> Account:
    optional_authentication_token = request.cookies.get(constants.AUTHENTICATION_TOKEN_COOKIE_NAME)
    if optional_authentication_token:
        return business_logic.get_account_for_jwt(optional_authentication_token)
    raise MissingAuthenticationTokenCookie()
