from http.client import HTTPException

from fastapi import Form, FastAPI
from starlette.responses import JSONResponse

from server import constants
from business_logic.errors import InvalidCredentialsError, AccountAlreadyExistsError
from business_logic.authentication_business_logic import AuthenticationBusinessLogic

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
                "message": "ServerError: "
                           f"Exception with name \"{exc.__class__.__name__}\" got raised but not handled.",
            }
        )


authentication_business_logic = AuthenticationBusinessLogic(
    path_to_accounts_yml_file=str(constants.PATH_TO_ACCOUNTS_YML_FILE),
)


@app.post("/login")  # ⚠️ Not RESTFULL
async def login(email: str = Form(), password: str = Form()) -> JSONResponse:
    return JSONResponse(
        content={
            "token": authentication_business_logic.unsafe_login(
                email=email, password=password
            ),
        }
    )


@app.post("/accounts")
async def register_account(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
) -> JSONResponse:
    account = authentication_business_logic.unsafe_register_account(
        name, email, password
    )
    return JSONResponse(
        content={
            "message": f"Account with name {account.name} was created."
        }
    )
