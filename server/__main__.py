from fastapi import FastAPI
from starlette.responses import JSONResponse
from errors import ServerError, AccountAlreadyExists, InvalidCredentials
from server.api_routers import api_router
from server.page_routers import page_router
from utils import (
    print_api_title,
)

app = FastAPI(
    title="Developer Dashboard API",
    on_startup=[print_api_title],
)

app.include_router(api_router)
app.include_router(page_router)


@app.exception_handler(ServerError)
async def server_error_exception_handler(_, exc: BaseException):
    if isinstance(exc, AccountAlreadyExists):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)},
        )
    if isinstance(exc, InvalidCredentials):
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
