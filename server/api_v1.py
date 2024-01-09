from http.client import HTTPException

from fastapi import Form, FastAPI
from starlette.responses import JSONResponse

from server import constants
from business_logic.errors import InvalidCredentialsError, AccountAlreadyExistsError
from business_logic._business_logic import BusinessLogic

app = FastAPI(
    title="Developer Dashboard API",
)


@app.exception_handler(HTTPException)
async def server_error_exception_handler(_, exc: HTTPException):
    if isinstance(exc, AccountAlreadyExistsError):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)},
        )
    if isinstance(exc, InvalidCredentialsError):
        return JSONResponse(
            status_code=403,
            content={"message": str(exc)},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"ServerError: "
                           f"Exception with name \"{exc.__name__}\" got raised but not handled.",
            }
        )


business_logic = BusinessLogic(
    path_to_accounts_yml_file=constants.PATH_TO_ACCOUNTS_YML_FILE,
    path_to_developers_json_file=constants.PATH_TO_DEVELOPERS_JSON_FILE,
    path_to_tasks_json_file=constants.PATH_TO_TASKS_JSON_FILE,
)


@app.get("/developers")
async def get_all_developers():
    all_developer_data = business_logic.unsafe_read_developer_data()
    return JSONResponse(
        content={
            "developers": [each.model_dump() for each in all_developer_data]
        }
    )


@app.get("/tasks")
async def get_all_tasks():
    all_tasks_data = business_logic.unsafe_read_task_data()
    return JSONResponse(
        content={
            "tasks": [each.model_dump() for each in all_tasks_data]
        }
    )


@app.post("/login")  # ⚠️ Not RESTFULL
async def login(email: str = Form(), password: str = Form()) -> JSONResponse:
    return JSONResponse(
        content={
            "token": business_logic.unsafe_login(
                email=email,
                password=password
            ),
        }
    )


@app.post("/accounts")
async def register_account(
        name: str = Form(),
        email: str = Form(),
        password: str = Form(),
) -> JSONResponse:
    account = business_logic.unsafe_register_account(name, email, password)
    return JSONResponse(
        content={
            "message": f"Account with name {account.name} was created."
        }
    )
