from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import make_html_element_from_file
from web_interface.private.types import HTMLElement


def make_css_style_sheet_link_html(file_name: str) -> HTMLElement:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "css-style-sheet-link.html",
        props={"file_name": file_name},
    )
