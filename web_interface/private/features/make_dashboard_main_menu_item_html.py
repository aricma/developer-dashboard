from web_interface.private.utils import make_html_template


def make_dashboard_main_menu_item_html(
    title: str,
    link: str,
    icon_id: str,
    is_active: bool = False,
) -> str:
    return make_html_template(
        template_name="dashboard-main-menu-item",
        props={
            "title": title,
            "link": link,
            "icon_id": icon_id,
            "active_class": "active" if is_active else None,
        },
    )
