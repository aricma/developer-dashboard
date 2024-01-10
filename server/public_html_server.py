from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse, FileResponse, RedirectResponse

from business_logic._business_logic import BusinessLogic
from server import constants
from server.authentication_utils import create_authentication_token_cookie_value, \
    create_expired_authentication_token_cookie_value
from web_interface.pages.make_register_page import make_register_page
from web_interface.pages.make_sign_in_page import make_sign_in_page

public_app = FastAPI(
    title="Developer Dashboard Web Server(Public)",
)

business_logic = BusinessLogic(
    path_to_accounts_yml_file=constants.PATH_TO_ACCOUNTS_YML_FILE,
    path_to_developers_json_file=constants.PATH_TO_DEVELOPERS_JSON_FILE,
    path_to_tasks_json_file=constants.PATH_TO_TASKS_JSON_FILE,
)


@public_app.get("/sign-in")
async def get_login_page() -> HTMLResponse:
    return HTMLResponse(
        content=make_sign_in_page()
    )


@public_app.post("/sign-in")
async def login(email: str = Form(), password: str = Form()) -> RedirectResponse:
    return redirect_after_successful_sign_in(
        authentication_token=business_logic.unsafe_login(email=email, password=password)
    )


@public_app.get("/sign-out")
async def logout() -> RedirectResponse:
    return RedirectResponse(
        status_code=303,
        url="/sign-in",
        headers={
            "Set-Cookie": create_expired_authentication_token_cookie_value()
        },
    )


@public_app.get("/register")
async def get_register_page() -> HTMLResponse:
    return HTMLResponse(
        content=make_register_page()
    )


@public_app.post("/register")
async def register(
        name: str = Form(),
        email: str = Form(),
        password: str = Form(),
) -> RedirectResponse:
    business_logic.unsafe_register_account(name, email, password)
    authentication_token = business_logic.unsafe_login(email=email, password=password)
    return redirect_after_successful_sign_in(authentication_token)


# ⚠️ this will serve everything
@public_app.get("/{file_path}")
async def serve_all_files_that_requested_by_html_files(file_path: str = None) -> FileResponse:
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(constants.PATH_TO_HTML_FILES / resolved_file_path)


def redirect_after_successful_sign_in(authentication_token: str) -> RedirectResponse:
    return RedirectResponse(
        status_code=303,
        url="/",
        headers={
            "Set-Cookie": create_authentication_token_cookie_value(authentication_token)
        },
    )
