import os
from pathlib import Path
from typing import Dict, List, Union, Optional
from uuid import uuid4
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.types import SkipMissingDict, KeepMissingDict


def print_html(html: str) -> None:
    print(BeautifulSoup(html, 'html.parser').prettify(
        formatter=HTMLFormatter(indent=4)
    ))


HTMLElement = Union[List["HTMLElement"], str, None]


def make_uuid():
    return str(uuid4())


Props = Dict[str, HTMLElement]


def make_html_template(template_name: str, props: Props = None) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / resolve_template_name(template_name),
        props=props if props is not None else {}
    )


def resolve_template_name(template_name: str) -> str:
    if not template_name.endswith(".html"):
        return template_name + ".html"
    if template_name.endswith("."):
        return template_name + "html"
    else:
        return template_name


def make_html_element_from_file(path: Union[Path, str], props: Props) -> str:
    with open(path, "r") as reader:
        template = reader.read()

    return fill_template_with_given_props_and_ignore_missing(
        template=template.strip(),
        props=resolve_and_filter_props(props)
    )


def resolve_and_filter_props(props: Props) -> Props:
    return {
        key: resolve_html_element(value)
        for key, value in props.items()
        if value is not None
    }


def fill_template_with_given_props_and_ignore_missing(template: str, props: Props) -> str:
    return template.format_map(SkipMissingDict(**props))


def partially_fill_template_with_only_given_props(template: str, props: Props) -> str:
    return template.format_map(KeepMissingDict(**props))


def resolve_html_element(html_element: HTMLElement) -> Optional[str]:
    if isinstance(html_element, str):
        return html_element
    if isinstance(html_element, list):
        return os.linesep.join([
            resolve_html_element(each)
            for each in html_element
            if each is not None
        ])
    return None


def join_html(html_items: List[str]) -> Optional[str]:
    return os.linesep.join(html_items)
