from typing import List, Optional

from web_interface.models import Alert
from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.components.make_dashboard_html import make_dashboard_html
from web_interface.private.components.make_warning_html import make_warning_html
from web_interface.private.features.make_dashboard_cards_html import (
    make_dashboard_cards_html,
)
from web_interface.private.features.make_overview_dashboard_card_html import (
    make_overview_dashboard_card_html,
)
from web_interface.private.utils import (
    read_text_file,
    join_html,
    HTMLElement,
)


def make_dashboard_overview_page(
    user_name: str,
    velocity_overview_chart_data_file_name: str,
    burn_down_overview_chart_data_file_name: str,
    velocity_warnings: Optional[List[Alert]] = None,
    burn_down_warnings: Optional[List[Alert]] = None,
) -> str:
    return make_dashboard_html(
        user_name=user_name,
        title="Overview",
        active_menu_link="/overview",
        content=[
            make_dashboard_cards_html(
                children=[
                    make_overview_dashboard_card_html(
                        title="Current Developer Velocity",
                        subtitle="An overview of the current developer velocity.",
                        children=[
                            make_chart_html(
                                data_file_name=velocity_overview_chart_data_file_name,
                                chart_type="velocity",
                            ),
                            make_warnings(warnings=velocity_warnings or []),
                        ],
                        description=read_text_file("velocity-overview"),
                        link="/velocity",
                        action_title="View Developer Velocity Details",
                    ),
                    make_overview_dashboard_card_html(
                        title="Current Burn Down Overview",
                        subtitle="An overview of the current task burn down estimation.",
                        children=[
                            make_chart_html(
                                data_file_name=burn_down_overview_chart_data_file_name,
                                chart_type="burn-down",
                            ),
                            make_warnings(warnings=burn_down_warnings or []),
                        ],
                        description=read_text_file("burn-down-overview"),
                        link="/burn-down",
                        action_title="View Task Burn Down Details",
                    ),
                ]
            ),
        ],
    )


def make_warnings(warnings: List[Alert]) -> HTMLElement:
    return join_html(
        [
            make_warning_html(
                title=each.title,
                description=each.description,
            )
            for each in warnings
        ]
    )
