from web_interface.private.utils import make_html_template


def make_error_html(
        error_code: str,
        message: str,
        action_link: str,
        action_title: str,
) -> str:
    return make_html_template(
        template_name="error",
        props={
            "error_code": error_code,
            "message": message,
            "action_link": action_link,
            "action_title": action_title,
        }
    )
