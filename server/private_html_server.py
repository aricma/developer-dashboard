import dataclasses
from http.client import HTTPException
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, FileResponse

from business_logic.authentication_business_logic import AuthenticationBusinessLogic
from business_logic.burn_down_business_logic import BurnDownBusinessLogic
from business_logic.burn_down_forecast_decimator import BurnDownForecastDecimator
from business_logic.chart_data_formatter import ChartDataFormatter
from business_logic.developer_velocity_business_logic import (
    DeveloperVelocityBusinessLogic,
)
from business_logic.developer_velocity_decimator import DeveloperVelocityDecimator
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.serializer.misc import Account
from server import constants
from server.authentication_utils import (
    create_authentication_token_cookie_value,
    authentication_token_is_valid,
    redirect_to_login_page,
)
from server.errors import (
    MissingAuthenticationTokenCookie,
    MissingAccountForAuthenticationToken,
)
from server.utils import limit_string
from web_interface.pages.make_dashboard_burn_down_page import (
    make_dashboard_burn_down_page,
)
from web_interface.pages.make_dashboard_overview_page import (
    make_dashboard_overview_page,
)
from web_interface.pages.make_dashboard_velocity_page import (
    make_dashboard_velocity_page,
)
from web_interface.pages.make_error_page import make_error_page
from server import envorinment

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
                message=f'There was an unknown error raised by the server: "{error_message}". '
                "Please create a ticket at https://github.com/aricma/developer-dashboard.",
            )
        )


developer_velocity_business_logic = DeveloperVelocityBusinessLogic(
    path_to_tasks_json_file=str(envorinment.TASK_DUMMY_DATA_FILE_PATH)
)

burn_down_business_logic = BurnDownBusinessLogic(
    path_to_tasks_json_file=str(envorinment.TASK_DUMMY_DATA_FILE_PATH)
)

chart_data_formatter = ChartDataFormatter(
    burn_down_forecast_decimator=BurnDownForecastDecimator(
        max_amount_of_data_points_per_forecast=20
    ),
    developer_velocity_decimator=DeveloperVelocityDecimator(
        max_amount_of_data_points_per_velocity=20
    ),
)

authentication_business_logic = AuthenticationBusinessLogic(
    path_to_accounts_yml_file=str(constants.PATH_TO_ACCOUNTS_YML_FILE),
)


@private_app.middleware("http")
async def check_for_authentication_cookie(request: Request, call_next):
    optional_authentication_token = request.cookies.get(
        constants.AUTHENTICATION_TOKEN_COOKIE_NAME
    )
    if optional_authentication_token is not None and authentication_token_is_valid(
        token=optional_authentication_token
    ):
        response = await call_next(request)
        try:
            new_authentication_token = (
                authentication_business_logic.unsafe_refresh_authentication_token(
                    old_authentication_token=optional_authentication_token
                )
            )
            response.headers["Set-Cookie"] = create_authentication_token_cookie_value(
                new_authentication_token
            )
            return response
        except Exception:
            raise MissingAccountForAuthenticationToken()
    return redirect_to_login_page()


@private_app.get("/dashboard/overview")
async def get_dashboard_overview_page(request: Request):
    account = _unsafe_get_account_from_authentication_token_cookie(request)
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
    account = _unsafe_get_account_from_authentication_token_cookie(request)
    two_weeks_of_developer_velocity = (
        developer_velocity_business_logic.get_developer_velocity(
            account=account,
            time_in_weeks=2,
        )
    )
    two_weeks_of_average_developer_velocity = (
        developer_velocity_business_logic.get_average_developer_velocity(
            time_in_weeks=2,
        )
    )
    four_weeks_of_developer_velocity = (
        developer_velocity_business_logic.get_developer_velocity(
            account=account,
            time_in_weeks=4,
        )
    )
    four_weeks_of_average_developer_velocity = (
        developer_velocity_business_logic.get_average_developer_velocity(
            time_in_weeks=4,
        )
    )
    eight_weeks_of_developer_velocity = (
        developer_velocity_business_logic.get_developer_velocity(
            account=account,
            time_in_weeks=8,
        )
    )
    eight_weeks_of_average_developer_velocity = (
        developer_velocity_business_logic.get_average_developer_velocity(
            time_in_weeks=8,
        )
    )
    return HTMLResponse(
        content=make_dashboard_velocity_page(
            user_name=account.name,
            last_two_weeks_velocity_chart_data_file_name=(
                _get_file_name_for_developer_velocity(
                    account_id=account.id,
                    developer_velocity=two_weeks_of_developer_velocity,
                    average_developer_velocity=two_weeks_of_average_developer_velocity,
                    tracking_start_date=Date.today().go_back_weeks(2),
                )
            ),
            last_four_weeks_velocity_chart_data_file_name=(
                _get_file_name_for_developer_velocity(
                    account_id=account.id,
                    developer_velocity=four_weeks_of_developer_velocity,
                    average_developer_velocity=four_weeks_of_average_developer_velocity,
                    tracking_start_date=Date.today().go_back_weeks(4),
                )
            ),
            last_eight_weeks_velocity_chart_data_file_name=(
                _get_file_name_for_developer_velocity(
                    account_id=account.id,
                    developer_velocity=eight_weeks_of_developer_velocity,
                    average_developer_velocity=eight_weeks_of_average_developer_velocity,
                    tracking_start_date=Date.today().go_back_weeks(8),
                )
            ),
        )
    )


def _get_file_name_for_developer_velocity(
    developer_velocity: DeveloperVelocity,
    average_developer_velocity: DeveloperVelocity,
    account_id: str,
    tracking_start_date: Date,
) -> str:
    chart_data = chart_data_formatter.to_single_developer_velocity_chart_data(
        developer_velocity=developer_velocity_business_logic.filter_velocity_before_given_start_date(
            velocity=developer_velocity,
            start_date=tracking_start_date,
        ),
        average_developer_velocity=developer_velocity_business_logic.filter_velocity_before_given_start_date(
            velocity=average_developer_velocity,
            start_date=tracking_start_date,
        ),
    )
    return developer_velocity_business_logic.get_file_path_for_data(
        data=dataclasses.asdict(chart_data),
        account_id=account_id,
    )


@private_app.get("/dashboard/burn-down")
async def get_dashboard_burn_down_page(request: Request):
    account = _unsafe_get_account_from_authentication_token_cookie(request)
    burn_down_forcast = burn_down_business_logic.get_task_burn_down_data_for_account()
    chart_data = chart_data_formatter.to_burn_down_chart_data(burn_down_forcast)
    file_name = developer_velocity_business_logic.get_file_path_for_data(
        data=dataclasses.asdict(chart_data),
        account_id=account.id,
    )
    return HTMLResponse(
        content=make_dashboard_burn_down_page(
            user_name=account.name, data_file_name=file_name
        )
    )


def _unsafe_get_account_from_authentication_token_cookie(request: Request) -> Account:
    optional_authentication_token = request.cookies.get(
        constants.AUTHENTICATION_TOKEN_COOKIE_NAME
    )
    if optional_authentication_token:
        account = authentication_business_logic.get_account_for_jwt(
            optional_authentication_token
        )
        if account:
            return account
        raise MissingAccountForAuthenticationToken()
    raise MissingAuthenticationTokenCookie()


@private_app.get("/{file_path}")
async def serve_all_files_that_requested_by_html_files(file_path: Optional[str] = None):
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(constants.PATH_TO_HTML_FILES / resolved_file_path)
