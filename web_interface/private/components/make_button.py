from web_interface.private.constants import PATH_TO_HTML_TEMPLATES
from web_interface.private.utils import make_html_element_from_file


def make_button(
        title: str
) -> str:
    return make_html_element_from_file(
        path=PATH_TO_HTML_TEMPLATES / "button.html",
        props={
            "title": title
        }
    )


if __name__ == '__main__':
    example_button = make_button(
        title="Foo",
    )
    print(example_button)
