from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import HTMLElement, make_html_element_from_file


def make_sign_out_button_html() -> HTMLElement:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "sign-out-button.html", props={}
    )
