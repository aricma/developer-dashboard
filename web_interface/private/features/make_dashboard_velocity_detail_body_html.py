from web_interface.private.utils import make_html_template


def make_dashboard_velocity_detail_body_html(
    description: str,
) -> str:
    return make_html_template(
        template_name="dashboard-velocity-detail-body",
        props={"description": description},
    )
