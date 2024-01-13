import dataclasses
from typing import List

from web_interface.private.components.make_accordion_html import make_accordion_html
from web_interface.private.components.make_accordion_item_html import (
    make_accordion_item_html,
)
from web_interface.private.components.make_burn_down_task_accordion_item_html import (
    make_burn_down_task_accordion_item_html,
)
from web_interface.private.utils import make_html_template, make_uuid


@dataclasses.dataclass
class BurnDownPageTask:
    name: str
    description: str
    assignees: List[str]
    story_points: float
    chart_data_file_name: str
    link_to_task_detail_page: str
    link_to_original_task_page: str
    estimated_finish_date: str


def make_dashboard_burn_down_detail_body_html(
    description: str, subtasks: List[BurnDownPageTask]
) -> str:
    accordion_id = "accordion-id-" + make_uuid()
    return make_html_template(
        template_name="dashboard-burn-down-detail-body",
        props={
            "description": description,
            "subtasks_html": [
                make_accordion_html(
                    accordion_id=accordion_id,
                    accordion_items=[
                        make_accordion_item_html(
                            accordion_id=accordion_id,
                            accordion_item_id="accordion_item_id-" + make_uuid(),
                            accordion_item_content_id="accordion_item_content_id-"
                            + make_uuid(),
                            accordion_title=task.name,
                            accordion_content=[
                                make_burn_down_task_accordion_item_html(
                                    description=task.description,
                                    link_to_task_detail_page=task.link_to_task_detail_page,
                                    chart_data_file_name=task.chart_data_file_name,
                                    assigned_developers=task.assignees,
                                    estimated_finish_date=task.estimated_finish_date,
                                    link_to_original_task=task.link_to_original_task_page,
                                )
                            ],
                        )
                        for task in subtasks
                    ],
                ),
            ],
        },
    )
