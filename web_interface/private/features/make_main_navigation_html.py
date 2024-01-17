from web_interface.private.components.make_flex_box_html import (
    make_flex_box_right_to_left,
)
from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.features.make_sign_out_button_html import (
    make_sign_out_button_html,
)
from web_interface.private.utils import make_html_element_from_file
from web_interface.private.types import HTMLElement


def make_main_navigation_html(
    main_navigation_items: HTMLElement = None,
) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "main-navigation.html",
        props={
            "main_navigation_items": main_navigation_items,
            "secondary_navigation_items": make_flex_box_right_to_left(
                children=make_sign_out_button_html(),
            ),
        },
    )
