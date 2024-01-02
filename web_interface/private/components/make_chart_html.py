from web_interface.private.utils import make_html_template


def make_chart_html() -> str:
    return make_html_template(
        template_name="chart",
        props={
        }
    )
