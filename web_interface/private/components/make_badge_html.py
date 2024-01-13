from web_interface.private.utils import make_html_template


def make_badge_html(value: str) -> str:
    return make_html_template(template_name="badge", props={"value": value})
