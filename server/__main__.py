from typing import Callable, Awaitable

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from server.constants import API_URL_PREFIX
from server.api_v1 import app as api_v1
from server.private_html_server import private_app as private_html_server
from server.public_html_server import public_app as public_html_server
from business_logic.utils import print_api_title

app = FastAPI(
    title="Developer Dashboard Application",
    on_startup=[print_api_title],
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

# do we need this here?
# should this be in api_v1?
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

re_routing_map = {
    "/": "/private/dashboard/overview",
    "/overview": "/private/dashboard/overview",
    "/dashboard": "/private/dashboard/overview",
    "/dashboard/overview": "/private/dashboard/overview",
    "/velocity": "/private/dashboard/velocity",
    "/dashboard/velocity": "/private/dashboard/velocity",
    "/burn-down": "/private/dashboard/burn-down",
    "/dashboard/burn-down": "/private/dashboard/burn-down",
    "/login": "/sign-in",
    "/log-in": "/sign-in",
    "/logout": "/sign-out",
    "/log-out": "/sign-out",
}


@app.middleware("http")
async def route_mapping(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    requested_path = request.url.path
    if requested_path in re_routing_map.keys():
        request.scope["path"] = re_routing_map[requested_path]

    return await call_next(request)


app.mount(API_URL_PREFIX, api_v1)
app.mount("/private", private_html_server)
app.mount("/", public_html_server)
