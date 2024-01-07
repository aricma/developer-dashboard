from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.features.make_dashboard_detail_header_html import make_dashboard_overview_detail_header_html
from web_interface.private.features.make_dashboard_main_menu_item_html import make_dashboard_main_menu_item_html
from web_interface.private.features.make_dashboard_velocity_detail_body_html import \
    make_dashboard_velocity_detail_body_html
from web_interface.private.utils import make_html_template, read_text_file


def make_dashboard_velocity_page(
        user_name: str,
        velocity_chart_data_file_name: str,
) -> str:
    return make_html_template(
        template_name="dashboard",
        props={
            "user_name": user_name,
            "main_menu_children": [
                make_dashboard_main_menu_item_html(
                    title="Overview",
                    link="/overview",
                    icon_id="house-fill",
                ),
                make_dashboard_main_menu_item_html(
                    title="Developer Velocity",
                    link="/velocity",
                    icon_id="speedometer",
                    is_active=True,
                ),
                make_dashboard_main_menu_item_html(
                    title="Task Burn Down Metric",
                    link="/burn-down",
                    icon_id="fire",
                ),
            ],
            "detail_children": [
                make_dashboard_overview_detail_header_html(
                    title="Developer Velocity"
                ),
                make_chart_html(
                    data_file_name=velocity_chart_data_file_name,
                    chart_type="velocity",
                ),
                make_dashboard_velocity_detail_body_html(
                    description=read_text_file("velocity-overview"),
                )
            ]
        }
    )
