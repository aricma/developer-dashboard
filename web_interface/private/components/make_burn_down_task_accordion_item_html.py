from typing import List

from web_interface.private.components.make_badge_html import make_badge_html
from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.utils import make_html_template


def make_burn_down_task_accordion_item_html(
    description: str,
    link_to_original_task: str,
    link_to_task_detail_page: str,
    chart_data_file_name: str,
    estimated_finish_date: str,
    assigned_developers: List[str],
) -> str:
    return make_html_template(
        template_name="burn-down-task-accordion-item",
        props={
            "description": description,
            "primary_action_link": link_to_task_detail_page,
            "primary_action_title": "Task Details",
            "secondary_action_link": link_to_original_task,
            "secondary_action_title": "Original Task",
            "action_link": link_to_task_detail_page,
            "action_title": "Go to task detail page",
            "chart_html": make_chart_html(
                data_file_name=chart_data_file_name,
                chart_type="burn-down",
            ),
            "estimated_finish_date": estimated_finish_date,
            "assigned_developers": [
                make_badge_html(value=developer) for developer in assigned_developers
            ],
        },
    )
