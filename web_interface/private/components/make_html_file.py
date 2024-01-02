from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import make_html_element_from_file, HTMLElement, resolve_html_element


def make_html_file(
    title: str,
    headers: HTMLElement = None,
    body: HTMLElement = None,
) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "html-file.html",
        props={
            "title": title,
            "headers": resolve_html_element(headers) or "",
            "body": resolve_html_element(body) or "",
        }
    )
