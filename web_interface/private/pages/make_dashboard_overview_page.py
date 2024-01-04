from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.components.make_warning_html import make_warning_html
from web_interface.private.features.make_dashboard_cards_html import make_dashboard_cards_html
from web_interface.private.features.make_dashboard_main_menu_item_html import make_dashboard_main_menu_item_html
from web_interface.private.features.make_dashboard_detail_header_html import make_dashboard_overview_detail_html
from web_interface.private.features.make_overview_dashboard_card_html import make_overview_dashboard_card_html
from web_interface.private.utils import make_html_template


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
                            description="The Developer Velocity shows the performance of the team. "
                                        "The Velocity should be constant. "
                                        "When the developer velocity drops, your teams has problems. "
                                        "It could be that the team is no longer motivated."
                                        "It could be that the estimations of the team are off, leading to a false velocity."
                                        "It could be that new team members disrupt the team dynamic."
                                        "In all cases is the code quality most likely dropping, which leads to false "
                                        "estimations for tasks that should take less to complete."
                                        "We recommend you find out what the team is thinking. "
                                        "Talk about the parts of the code that need refactoring."
                                        "On the other hand if the velocity is up it might be that the developers are not "
                                        "spending enough time keeping the code clean. "
                                        "This will slow your team down in the long run. "
                                        "We recommend you spend more time cleaning your code. "
                                        "Else you will see the velocity drop soon enough.",
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
                            description="The Task Burn Down Metric shows the estimated delivery time for the current tasks. "
                                        "You can check here if your team is on track and will finish their tasks on time. "
                                        "If you burn down chart shows a stagnating task delivery time you should make sure "
                                        "management is informed. "
                                        "The Task Burn Down Metric should only increase if the scope of your task increased. "
                                        "This includes an unforeseen increase in scope do to technical difficulties. "
                                        "If you team has a tanking velocity your Task Burn Down Metric will move up. "
                                        "We recommend you make sure the team is spending their time writing clean code to "
                                        "get the velocity back up. "
                                        "Make sure you never have a Task Burn Down Metric the is constantly rising. "
                                        "It means the project will never finish and you have to cut down the scope and "
                                        "introduce a feature stop until the chart is falling again.",
                            link="/burn-down",
                            action_title="View Task Burn Down Details"
                        ),
                    ]
                ),
            ]
        }
    )
