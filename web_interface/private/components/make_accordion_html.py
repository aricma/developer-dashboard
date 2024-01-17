from web_interface.private.utils import make_html_template
from web_interface.private.types import HTMLElement


def make_accordion_html(accordion_id: str, accordion_items: HTMLElement) -> str:
    return make_html_template(
        template_name="accordion",
        props={"accordion_id": accordion_id, "accordion_items": accordion_items},
    )
