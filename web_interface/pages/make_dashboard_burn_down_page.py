from typing import List

from web_interface.private.components.make_chart_html import make_chart_html
from web_interface.private.components.make_dashboard_html import make_dashboard_html
from web_interface.private.features.make_dashboard_burn_down_detail_body_html import (
    make_dashboard_burn_down_detail_body_html,
    BurnDownPageTask,
)
from web_interface.private.utils import (
    read_text_file,
)


def make_dashboard_burn_down_page(
    user_name: str,
    data_file_name: str,
    burn_down_tasks: List[BurnDownPageTask],
) -> str:
    return make_dashboard_html(
        user_name=user_name,
        title="Task Burn Down Estimation",
        content=[
            make_chart_html(
                data_file_name=data_file_name,
                chart_type="burn-down",
            ),
            make_dashboard_burn_down_detail_body_html(
                description=read_text_file("burn-down-overview"),
                subtasks=burn_down_tasks,
            ),
        ],
    )
