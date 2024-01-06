from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.components.make_warning_html import make_warning_html
from web_interface.private.features.make_dashboard_cards_html import make_dashboard_cards_html
from web_interface.private.features.make_dashboard_main_menu_item_html import make_dashboard_main_menu_item_html
from web_interface.private.features.make_dashboard_detail_header_html import make_dashboard_overview_detail_html
from web_interface.private.features.make_overview_dashboard_card_html import make_overview_dashboard_card_html
from web_interface.private.utils import (
    make_html_template,
    read_text_file,
)


def make_dashboard_overview_page(
        user_name: str,
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
                    is_active=True,
                ),
                make_dashboard_main_menu_item_html(
                    title="Developer Velocity",
                    link="/velocity",
                    icon_id="speedometer",
                ),
                make_dashboard_main_menu_item_html(
                    title="Task Burn Down Metric",
                    link="/burn-down",
                    icon_id="fire",
                ),
            ],
            "detail_children": [
                make_dashboard_overview_detail_html(
                    title="Overview"
                ),
                make_dashboard_cards_html(
                    children=[
                        make_overview_dashboard_card_html(
                            title="Current Developer Velocity",
                            subtitle="An overview of the current developer velocity.",
                            children=make_chart_html(
                                data_file_name="./foobar-developer-velocity.json",
                                chart_type="velocity",
                            ),
                            description=read_text_file("velocity-overview"),
                            link="/velocity",
                            action_title="View Developer Velocity Details"
                        ),
                        make_overview_dashboard_card_html(
                            title="Current Burn Down Overview",
                            subtitle="An overview of the current task burn down metric.",
                            children=[
                                make_chart_html(
                                    data_file_name="./foobar-task-burn-down-metric.json",
                                    chart_type="burn-down",
                                ),
                                make_warning_html(
                                    title="Rising Task Burn Down Metric",
                                    description="Attention you have a rising Task Burn Down Metric. "
                                                "Make sure this happened because of changes in scope.",
                                ),
                            ],
                            description=read_text_file("burn-down-overview"),
                            link="/burn-down",
                            action_title="View Task Burn Down Details"
                        ),
                    ]
                ),
            ]
        }
    )
