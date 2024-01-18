import dataclasses
import statistics
from http.client import HTTPException
from typing import Optional, List, Callable, Awaitable

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, FileResponse, Response

from business_logic.authentication_business_logic import AuthenticationBusinessLogic
from business_logic.burn_down_business_logic import BurnDownBusinessLogic
from business_logic.burn_down_forecast_decimator import BurnDownForecastDecimator
from business_logic.burn_down_forecastable_task_getter_proxy import (
    BurnDownForecastableTaskGetterProxy,
)
from business_logic.caching_task_getter import CachingTaskGetter, TaskCache, CacheUtils, TasksCache
from server.chart_data_formatter import ChartDataFormatter
from business_logic.developer_velocity_business_logic import (
    DeveloperVelocityBusinessLogic,
)
from business_logic.developer_velocity_decimator import DeveloperVelocityDecimator
from business_logic.dummy_data_task_getter import DummyDataFileTaskGetter
from business_logic.models.burn_down_forecast import BurnDownForecast
from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.serializer.misc import Account
from business_logic.velocity_trackable_task_getter_proxy import (
    VelocityTrackableTaskGetterProxy,
)
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
from web_interface.private.features.make_dashboard_burn_down_detail_body_html import BurnDownPageTask

private_app = FastAPI(
    title="Developer Dashboard Web Server(Private)",
)


@private_app.exception_handler(HTTPException)
async def server_error_exception_handler(_: Request, exc: HTTPException) -> Response:
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


dummy_data_file_task_getter = DummyDataFileTaskGetter(
    path_to_dummy_data=str(envorinment.PATH_TO_TASK_DUMMY_DATA)
)
velocity_trackable_task_getter = VelocityTrackableTaskGetterProxy(
    task_getter=dummy_data_file_task_getter
)
caching_velocity_trackable_task_getter = CachingTaskGetter(
    task_getter=velocity_trackable_task_getter,
    task_cache=TaskCache(
        cache_utils=CacheUtils(),
        cache_life_time_in_seconds=30,
    ),
    tasks_cache=TasksCache(
        cache_utils=CacheUtils(),
        cache_life_time_in_seconds=45,
    )
)
developer_velocity_business_logic = DeveloperVelocityBusinessLogic(
    task_getter=caching_velocity_trackable_task_getter
)

burn_down_forecastable_task_getter = BurnDownForecastableTaskGetterProxy(
    task_getter=dummy_data_file_task_getter
)
caching_burn_down_forecastable_task_getter = CachingTaskGetter(
    task_getter=burn_down_forecastable_task_getter,
    task_cache=TaskCache(
        cache_utils=CacheUtils(),
        cache_life_time_in_seconds=30,
    ),
    tasks_cache=TasksCache(
        cache_utils=CacheUtils(),
        cache_life_time_in_seconds=45,
    )
)

burn_down_business_logic = BurnDownBusinessLogic(
    dummy_data_file_task_getter=dummy_data_file_task_getter,
    developer_velocity_business_logic=developer_velocity_business_logic,
    burn_down_forecastable_task_getter=caching_burn_down_forecastable_task_getter,
)

detail_page_chart_data_formatter = ChartDataFormatter(
    burn_down_forecast_decimator=BurnDownForecastDecimator(
        max_amount_of_data_points_per_forecast=20
    ),
    developer_velocity_decimator=DeveloperVelocityDecimator(
        max_amount_of_data_points_per_velocity=20
    ),
)

overview_chart_data_formatter = ChartDataFormatter(
    burn_down_forecast_decimator=BurnDownForecastDecimator(
        max_amount_of_data_points_per_forecast=10
    ),
    developer_velocity_decimator=DeveloperVelocityDecimator(
        max_amount_of_data_points_per_velocity=10
    ),
)

authentication_business_logic = AuthenticationBusinessLogic(
    path_to_accounts_yml_file=str(constants.PATH_TO_ACCOUNTS_YML_FILE),
)


@private_app.middleware("http")
async def check_for_authentication_cookie(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
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
async def get_dashboard_overview_page(request: Request) -> HTMLResponse:
    account = _unsafe_get_account_from_authentication_token_cookie(request)
    return HTMLResponse(
        content=make_dashboard_overview_page(
            user_name=account.name,
            velocity_overview_chart_data_file_name=_get_velocity_overview_chart_data_file_name(
                account=account,
            ),
            burn_down_overview_chart_data_file_name=_get_total_task_burn_down_data_file_name(
                account_id=account.id,
            ),
        )
    )


def _get_velocity_overview_chart_data_file_name(account: Account) -> str:
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
    tracking_start_date = Date.today().go_back_weeks(2)
    chart_data = overview_chart_data_formatter.to_single_developer_velocity_chart_data(
        developer_velocity=developer_velocity_business_logic.filter_velocity_before_given_start_date(
            velocity=two_weeks_of_developer_velocity,
            start_date=tracking_start_date,
        ),
        average_developer_velocity=developer_velocity_business_logic.filter_velocity_before_given_start_date(
            velocity=two_weeks_of_average_developer_velocity,
            start_date=tracking_start_date,
        ),
    )
    return developer_velocity_business_logic.get_file_path_for_data(
        data=dataclasses.asdict(chart_data),
        account_id=account.id,
    )


@private_app.get("/dashboard/velocity")
async def get_dashboard_velocity_page(request: Request) -> HTMLResponse:
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
    chart_data = detail_page_chart_data_formatter.to_single_developer_velocity_chart_data(
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
async def get_dashboard_burn_down_page(request: Request) -> HTMLResponse:
    account = _unsafe_get_account_from_authentication_token_cookie(request)
    file_name = _get_total_task_burn_down_data_file_name(
        account_id=account.id,
    )
    burn_down_tasks: List[BurnDownPageTask] = []
    all_burn_down_forcastable_tasks = (
        burn_down_business_logic.get_all_burn_down_forecastable_tasks()
    )
    median_developer_velocity_of_the_average_developer_for_the_last_eight_weeks: float = statistics.median(
        developer_velocity_business_logic.get_average_developer_velocity(
            time_in_weeks=8
        ).values()
    )
    for task in all_burn_down_forcastable_tasks:
        burn_down_forecast = burn_down_business_logic.get_task_burn_down_data(
            task_id=task.id,
            developer_velocity_as_story_points_per_day=(
                median_developer_velocity_of_the_average_developer_for_the_last_eight_weeks
            ),
        )
        if burn_down_forecast is None:
            raise TaskNotFound(task_id=task.id)
        chart_data_for_task = detail_page_chart_data_formatter.to_burn_down_chart_data(
            burn_down_forecast
        )
        chart_data_file_name = developer_velocity_business_logic.get_file_path_for_data(
            data=dataclasses.asdict(chart_data_for_task),
            account_id=account.id,
        )
        estimated_finish_date = _get_last_date_from_burn_down_forecast(
            burn_down_forecast
        )
        burn_down_tasks.append(
            BurnDownPageTask(
                name=task.name,
                description=task.description,
                assignees=task.assignees,
                story_points=task.story_points,
                chart_data_file_name=chart_data_file_name,
                link_to_task_detail_page=f"/{task.id}",
                estimated_finish_date=(
                    Date.from_string(estimated_finish_date).to_human_readable()
                    if estimated_finish_date is not None
                    else "No finish date estimated"
                ),
                link_to_original_task_page="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dl?retiredLocale=de",
            )
        )
    return HTMLResponse(
        content=make_dashboard_burn_down_page(
            user_name=account.name,
            data_file_name=file_name,
            burn_down_tasks=burn_down_tasks,
        )
    )


def _get_total_task_burn_down_data_file_name(account_id: str) -> str:
    burn_down_forcast = burn_down_business_logic.get_total_task_burn_down_data()
    chart_data = detail_page_chart_data_formatter.to_burn_down_chart_data(
        burn_down_forcast
    )
    return developer_velocity_business_logic.get_file_path_for_data(
        data=dataclasses.asdict(chart_data),
        account_id=account_id,
    )


class TaskNotFound(ValueError, HTTPException):
    def __init__(self, task_id: str):
        super().__init__(f'No task was found for given task_id: "{task_id}".')


def _get_last_date_from_burn_down_forecast(
        burn_down_forecast: BurnDownForecast,
) -> Optional[str]:
    last_date = None
    for each in burn_down_forecast.keys():
        next_date = Date.from_string(each)
        if last_date is None:
            last_date = next_date
        elif next_date > last_date:
            last_date = next_date
    if last_date is None:
        return None
    return last_date.to_string()


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
async def serve_all_files_that_requested_by_html_files(file_path: Optional[str] = None) -> FileResponse:
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(constants.PATH_TO_HTML_FILES / resolved_file_path)
