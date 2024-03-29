from web_interface.private.utils import make_html_template
from web_interface.private.types import HTMLElement


def make_dashboard_cards_html(children: HTMLElement = None) -> str:
    return make_html_template(
        template_name="dashboard-overview-cards", props={"children": children}
    )
