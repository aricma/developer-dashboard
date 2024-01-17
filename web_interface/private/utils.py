import os
from pathlib import Path
from typing import List, Union, Optional, Literal
from uuid import uuid4
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from web_interface.private.constants import PATH_TO_HTML_TEMPLATES, PATH_TO_TEXT_FILES
from web_interface.private.types import SkipMissingDict, KeepMissingDict, HTMLElement, Props


def print_html(html: str) -> None:
    print(
        BeautifulSoup(html, "html.parser").prettify(
            formatter=HTMLFormatter(indent=4)  # type: ignore
            # I looked up the issue on stack overflow and found out that
            # I have to use 4.11 to use the HTMLFormatter with the indent option
            # I am already using version 4.12 for bs4 and also the types ...
            # I decided to type ignore since this does not raise any errors
            # only mypy is complaining
            # here the stack overflow link https://stackoverflow.com/a/72746676
        )
    )


def make_uuid():
    return str(uuid4())


def make_html_template(template_name: str, props: Optional[Props] = None) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / resolve_template_name(template_name),
        props={} if props is None else props,
    )


def resolve_template_name(template_name: str) -> str:
    return resolve_file_name(file_name=template_name, extension="html")


FileExtension = Union[
    Literal["html"],
    Literal["txt"],
]


def resolve_file_name(file_name: str, extension: FileExtension) -> str:
    if not file_name.endswith("." + extension):
        return file_name + "." + extension
    if file_name.endswith("."):
        return file_name + extension
    else:
        return file_name


def make_html_element_from_file(path: Union[Path, str], props: Props) -> str:
    with open(path, "r") as reader:
        template = reader.read()

    return fill_template_with_given_props_and_ignore_missing(
        template=template.strip(), props=resolve_and_filter_props(props)
    )


def resolve_and_filter_props(props: Props) -> Props:
    return {
        key: resolve_html_element(value)
        for key, value in props.items()
        if value is not None
    }


def fill_template_with_given_props_and_ignore_missing(
    template: str, props: Props
) -> str:
    return template.format_map(SkipMissingDict(**props))


def partially_fill_template_with_only_given_props(template: str, props: Props) -> str:
    return template.format_map(KeepMissingDict(**props))


def resolve_html_element(html_element: HTMLElement) -> Optional[str]:
    if isinstance(html_element, str):
        return html_element
    if isinstance(html_element, list):
        resolved_elements = []
        for each in html_element:
            if each is None:
                continue
            resolved_element = resolve_html_element(each)
            if resolved_element is None:
                continue
            resolved_elements.append(resolved_element)

        return os.linesep.join(resolved_elements)
    return None


def join_html(html_items: List[str]) -> Optional[str]:
    if len(html_items) == 0:
        return None
    return os.linesep.join(html_items)


def read_text_file(text_file_name: str) -> str:
    return read_file(PATH_TO_TEXT_FILES / resolve_text_file_name(text_file_name))


def resolve_text_file_name(text_file_name: str) -> str:
    return resolve_file_name(file_name=text_file_name, extension="txt")


def read_file(path: Union[Path, str]) -> str:
    with open(path, "r") as reader:
        return reader.read()
