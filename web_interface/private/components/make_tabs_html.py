from web_interface.private.utils import make_html_template
from web_interface.private.types import HTMLElement


def make_tabs_content_html(children: HTMLElement) -> str:
    return make_html_template(
        template_name="tabs-content", props={"children": children}
    )


def make_tab_panel_html(
    panel_id: str,
    children: HTMLElement,
    initially_active: bool = False,
) -> str:
    return make_html_template(
        template_name="tab-panel",
        props={
            "panel_id": panel_id,
            "children": children,
            "active_class": "active show" if initially_active else None,
        },
    )


def make_tabs_html(
    children: HTMLElement,
) -> str:
    return make_html_template(
        template_name="tabs",
        props={
            "children": children,
        },
    )


def make_tab_html(panel_id: str, title: str, initially_selected: bool = False) -> str:
    return make_html_template(
        template_name="tab",
        props={
            "panel_id": panel_id,
            "active_class": "active" if initially_selected else None,
            "is_selected": "true" if initially_selected else "false",
            "title": title,
        },
    )
