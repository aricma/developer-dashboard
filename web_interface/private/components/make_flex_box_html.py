from typing import Union, Literal

from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.models import Alignment
from web_interface.private.utils import (
    make_html_element_from_file,
    HTMLElement,
    resolve_html_element,
    make_html_template,
)


def make_flex_box_center_html(
    children: HTMLElement,
) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "flex-box-center.html",
        props={
            "children": resolve_html_element(children),
        },
    )


def make_flex_box_right_to_left(children: HTMLElement) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "flex-box-right-to-left.html",
        props={"children": children},
    )


Direction = Union[Literal["row"], Literal["col"]]


def make_flex_box_html(
    children: HTMLElement,
    direction: Direction = "col",
    alignment: Alignment = "center",
) -> str:
    return make_html_template(
        template_name="flex-box",
        props={
            "children": children,
            "direction_class": direction,
            "alignment_class": f"justify-content-{alignment}",
        },
    )
