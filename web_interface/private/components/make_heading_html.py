from typing import Union, Literal

from web_interface.private.models import Alignment
from web_interface.private.utils import make_html_template
from web_interface.private.types import SkipMissingDict

Heading = Union[
    Literal["h1"],
    Literal["h2"],
    Literal["h3"],
    Literal["h4"],
    Literal["h5"],
    Literal["h6"],
]


heading_to_classes_map = {
    "h1": "mb-4",
    "h2": "mb-3",
    "h3": "mb-2",
    "h4": "mb-1",
    "h5": "",
    "h6": "",
}

alignment_to_classes_map = SkipMissingDict(
    **{
        "start": "text-start",
        "center": "text-center",
        "end": "text-end",
    }
)


def make_heading_html(
    title: str, heading: Heading = "h2", alignment: Alignment = "start"
) -> str:
    return make_html_template(
        template_name="heading",
        props={
            "title": title,
            "heading_tag": heading,
            "classes": _make_classes(
                heading_to_classes_map[heading], alignment_to_classes_map[alignment]
            ),
        },
    )


def _make_classes(*classes: str) -> str:
    return " ".join(classes)
