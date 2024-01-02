from web_interface.private.components.make_html_file import make_html_file
from web_interface.private.features.make_error_html import make_error_html


def make_error_page(
        error_code: str,
        message: str,
) -> str:
    return make_html_file(
        title=f"Developer Dashboard | {error_code}",
        body=make_error_html(
            error_code=error_code,
            message=message,
            action_link="/dashboard",
            action_title="Return Back To Dashboard",
        ),
    )
