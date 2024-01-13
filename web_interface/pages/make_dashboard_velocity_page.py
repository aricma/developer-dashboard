from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.components.make_dashboard_html import make_dashboard_html
from web_interface.private.components.make_tabs_html import (
    make_tabs_content_html,
    make_tab_panel_html,
    make_tabs_html,
    make_tab_html,
)
from web_interface.private.features.make_dashboard_velocity_detail_body_html import (
    make_dashboard_velocity_detail_body_html,
)
from web_interface.private.utils import read_text_file


def make_dashboard_velocity_page(
    user_name: str,
    last_two_weeks_velocity_chart_data_file_name: str,
    last_four_weeks_velocity_chart_data_file_name: str,
    last_eight_weeks_velocity_chart_data_file_name: str,
) -> str:
    return make_dashboard_html(
        user_name=user_name,
        title="Developer Velocity",
        active_menu_link="/velocity",
        content=[
            make_tabs_html(
                children=[
                    make_tab_html(
                        panel_id="last-two-weeks",
                        title="Last 2 Weeks",
                        initially_selected=True,
                    ),
                    make_tab_html(
                        panel_id="last-four-weeks",
                        title="Last 4 Weeks",
                    ),
                    make_tab_html(
                        panel_id="last-eight-weeks",
                        title="Last 8 Weeks",
                    ),
                ]
            ),
            make_tabs_content_html(
                children=[
                    make_tab_panel_html(
                        panel_id="last-two-weeks",
                        children=[
                            make_chart_html(
                                data_file_name=last_two_weeks_velocity_chart_data_file_name,
                                chart_type="velocity",
                            ),
                        ],
                        initially_active=True,
                    ),
                    make_tab_panel_html(
                        panel_id="last-four-weeks",
                        children=[
                            make_chart_html(
                                data_file_name=last_four_weeks_velocity_chart_data_file_name,
                                chart_type="velocity",
                            ),
                        ],
                    ),
                    make_tab_panel_html(
                        panel_id="last-eight-weeks",
                        children=[
                            make_chart_html(
                                data_file_name=last_eight_weeks_velocity_chart_data_file_name,
                                chart_type="velocity",
                            ),
                        ],
                    ),
                ]
            ),
            make_dashboard_velocity_detail_body_html(
                description=read_text_file("velocity-detail-description"),
            ),
        ],
    )
