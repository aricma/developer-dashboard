from web_interface.private.utils import make_html_template, HTMLElement


def make_overview_dashboard_card_html(
        title: str,
        subtitle: str,
        description: str,
        link: str,
        action_title: str,
        children: HTMLElement = None
) -> str:
    return make_html_template(
        template_name="dashboard-overview-card",
        props={
            "title": title,
            "subtitle": subtitle,
            "description": description,
            "link": link,
            "action_title": action_title,
            "children": children
        }
    )
