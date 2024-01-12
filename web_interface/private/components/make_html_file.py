from web_interface.private.utils import (
    HTMLElement,
    resolve_html_element,
    make_html_template,
)


def make_html_file(
    title: str,
    headers: HTMLElement = None,
    body: HTMLElement = None,
) -> str:
    return make_html_template(
        template_name="html-file",
        props={
            "title": title,
            "headers": resolve_html_element(headers),
            "body": resolve_html_element(body),
        },
    )
