from web_interface.private.utils import make_html_template
from web_interface.private.types import HTMLElement


def make_header_main_footer_html(
    header: HTMLElement = None,
    main: HTMLElement = None,
    footer: HTMLElement = None,
) -> str:
    return make_html_template(
        template_name="header-main-footer",
        props={
            "header": header,
            "main": main,
            "footer": footer,
        },
    )
