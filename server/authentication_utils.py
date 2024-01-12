from starlette.responses import RedirectResponse

from server import constants


def create_authentication_token_cookie_value(token: str) -> str:
    return (
        f"{constants.AUTHENTICATION_TOKEN_COOKIE_NAME}={token};"
        f"Max-Age={constants.AUTHENTICATION_TOKEN_COOKIE_LIFE_TIME_IN_SECONDS};"
        "HttpOnly;"  # to prevent XSS attacks
        "Secure;"  # to prevent Network Eavesdropping attacks
        "SameSite=Strict;"  # to prevent CSRF attacks
    )


def create_expired_authentication_token_cookie_value() -> str:
    return (
        f"{constants.AUTHENTICATION_TOKEN_COOKIE_NAME}=;"
        f"Max-Age=-1;"


def redirect_after_successful_sign_in(authentication_token: str) -> RedirectResponse:
    return RedirectResponse(
        status_code=303,
        url="/",
        headers={
            "Set-Cookie": create_authentication_token_cookie_value(authentication_token)
        },
    )
    )
