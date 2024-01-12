from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import make_html_element_from_file


def make_register_form_html(link_to_login_form: str) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "register-form.html",
        props={"link_to_login_form": link_to_login_form},
    )
