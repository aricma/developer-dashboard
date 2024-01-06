from web_interface.private.utils import make_html_template


def make_dashboard_overview_detail_header_html(
        title: str
) -> str:
    return make_html_template(
        template_name="dashboard-detail-header",
        props={
            "title": title
        }
    )
