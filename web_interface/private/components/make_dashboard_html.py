from web_interface.private.features.make_dashboard_detail_header_html import (
    make_dashboard_overview_detail_header_html,
)
from web_interface.private.features.make_dashboard_main_menu_item_html import (
    make_dashboard_main_menu_item_html,
)
from web_interface.private.utils import HTMLElement, make_html_template


def make_dashboard_html(
    user_name: str,
    title: str,
    content: HTMLElement,
    active_menu_link: str,
) -> str:
    return make_html_template(
        template_name="dashboard",
        props={
            "user_name": user_name,
            "main_menu_children": [
                make_dashboard_main_menu_item_html(
                    title="Overview",
                    link="/overview",
                    icon_id="house-fill",
                    is_active=active_menu_link == "/overview",
                ),
                make_dashboard_main_menu_item_html(
                    title="Developer Velocity",
                    link="/velocity",
                    icon_id="speedometer",
                    is_active=active_menu_link == "/velocity",
                ),
                make_dashboard_main_menu_item_html(
                    title="Task Burn Down Estimation",
                    link="/burn-down",
                    icon_id="fire",
                    is_active=active_menu_link == "/burn-down",
                ),
            ],
            "detail_children": [
                make_dashboard_overview_detail_header_html(title=title),
                content,
            ],
        },
    )
