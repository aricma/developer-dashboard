from web_interface.private.utils import make_html_template


def make_warning_html(
    title: str,
    description: str,
) -> str:
    return make_html_template(
        template_name="warning",
        props={
            "title": title,
            "description": description,
        },
    )
