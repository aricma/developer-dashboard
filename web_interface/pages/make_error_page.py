from web_interface.private.components.make_footer_center_html import make_footer_center_html
from web_interface.private.components.make_header_main_footer_html import make_header_main_footer_html
from web_interface.private.components.make_html_file import make_html_file
from web_interface.private.features.make_error_html import make_error_html
from web_interface.private.features.make_public_page_html import make_public_page_html


def make_error_page(
        error_code: str,
        message: str,
) -> str:
    return make_html_file(
        title=f"Developer Dashboard | {error_code}",
        body=[
            make_header_main_footer_html(
                header=make_public_page_html(),
                main=make_error_html(
                    error_code=error_code,
                    message=message,
                    action_link="/dashboard",
                    action_title="Return Back To Dashboard",
                ),
                footer=make_footer_center_html()
            ),
        ]
    )
