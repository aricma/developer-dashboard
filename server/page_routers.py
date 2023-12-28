from typing import Optional

from fastapi import APIRouter
from starlette.responses import HTMLResponse, FileResponse

from constants import PATH_TO_HTML_FILES

page_router = APIRouter()


@page_router.get("/")
async def get_index():
    with open(PATH_TO_HTML_FILES / "index.html", "rb") as reader:
        return HTMLResponse(
            content=reader.read()
        )


@page_router.get("/login")
async def get_login_page():
    with open(PATH_TO_HTML_FILES / "login.html", "rb") as reader:
        return HTMLResponse(
            content=reader.read()
        )


@page_router.get("/register")
async def get_register_page():
    with open(PATH_TO_HTML_FILES / "register.html", "rb") as reader:
        return HTMLResponse(
            content=reader.read()
        )


# this one is serving all the css and js files
@page_router.get("/{file_path}")
async def catch_all(file_path: Optional[str]):
    resolved_file_path = "index.html" if not file_path else file_path
    return FileResponse(PATH_TO_HTML_FILES / resolved_file_path)
