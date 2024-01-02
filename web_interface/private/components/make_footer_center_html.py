from web_interface.private.utils import make_html_template


def make_footer_center_html() -> str:
    return make_html_template(
        template_name="footer-center",
    )
