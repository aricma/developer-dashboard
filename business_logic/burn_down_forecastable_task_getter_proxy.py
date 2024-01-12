from typing import List

from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.burn_down_forecastable_task import BurnDownForecastableTask
from business_logic.models.task import Task


class BurnDownForecastableTaskGetterProxy(TaskGetter[BurnDownForecastableTask]):
    def __init__(self, task_getter: TaskGetter[Task]):
        self._task_getter = task_getter

    def get_tasks(self) -> List[BurnDownForecastableTask]:
        return [
            self._to_burn_down_forecastable_task(task)
            for task in self._task_getter.get_tasks()
            if task.date_finished is None
        ]

    @staticmethod
    def _to_burn_down_forecastable_task(task: Task) -> BurnDownForecastableTask:
        return BurnDownForecastableTask(
            id=task.id,
            story_points=task.story_points,
            date_started=task.date_started,
        )
