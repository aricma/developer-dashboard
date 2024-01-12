from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import make_html_element_from_file


def make_login_form_html(link_to_register_form: str) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "sign-in-form.html",
        props={"link_to_register_form": link_to_register_form},
    )
