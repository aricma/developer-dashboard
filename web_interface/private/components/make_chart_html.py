from web_interface.private.utils import make_html_template


def make_chart_html(
        data_file_name: str,
) -> str:
    return make_html_template(
        template_name="chart",
        props={
            "data_file_name": data_file_name,
        }
    )
