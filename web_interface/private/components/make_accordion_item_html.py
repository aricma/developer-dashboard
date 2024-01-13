from web_interface.private.utils import make_html_template, HTMLElement


def make_accordion_item_html(
    accordion_id: str,
    accordion_item_id: str,
    accordion_item_content_id: str,
    accordion_title: HTMLElement,
    accordion_content: HTMLElement,
) -> str:
    return make_html_template(
        template_name="accordion-item",
        props={
            "accordion_id": accordion_id,
            "accordion_item_id": accordion_item_id,
            "accordion_item_content_id": accordion_item_content_id,
            "accordion_title": accordion_title,
            "accordion_content": accordion_content,
        },
    )
