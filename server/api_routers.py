import jwt
from fastapi import APIRouter, Form
from pydantic import BaseModel
from starlette.responses import JSONResponse

import constants
from errors import InvalidCredentials
from models import AccountRequest
from business_logic import BusinessLogic

api_router = APIRouter(
    prefix=constants.API_URL_PREFIX
)

business_logic = BusinessLogic(
    path_to_accounts_yml_file=constants.PATH_TO_ACCOUNTS_YML_FILE,
    path_to_developers_json_file=constants.PATH_TO_DEVELOPERS_JSON_FILE,
    path_to_tasks_json_file=constants.PATH_TO_TASKS_JSON_FILE,
)


@api_router.get("/developers")
async def get_all_developers():
    all_developer_data = business_logic.unsafe_read_developer_data()
    return JSONResponse(
        content={
            "developers": [each.model_dump() for each in all_developer_data]
        }
    )


@api_router.get("/tasks")
async def get_all_tasks():
    all_tasks_data = business_logic.unsafe_read_task_data()
    return JSONResponse(
        content={
            "tasks": [each.model_dump() for each in all_tasks_data]
        }
    )


@api_router.post("/login")
async def login(email: str = Form(), password: str = Form()) -> JSONResponse:
    account = business_logic.get_account_for_email(email=email)

    if not account:
        raise InvalidCredentials()

    password_is_valid = business_logic.validate_password_against_account(
        account=account,
        password=password
    )

    if not password_is_valid:
        raise InvalidCredentials()

    token = jwt.encode(
        payload={
            "name": account.name,
            "email": account.email,
            "permissions": list(account.permissions)
        },
        key='secret',
        algorithm="HS256"
    )

    return JSONResponse(
        content={
            "token": token,
        }
    )


@api_router.post("/accounts")
async def register_account(
        name: str = Form(),
        email: str = Form(),
        password: str = Form(),
) -> JSONResponse:
    account = business_logic.unsafe_register_account(request=AccountRequest(**{
        "name": name,
        "email": email,
        "password": password,
    }))

    return JSONResponse(
        content={
            "message": f"Account with name {account.name} was created."
        }
    )
