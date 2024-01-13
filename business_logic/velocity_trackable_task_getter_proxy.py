from typing import List, Optional

from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.date import Date
from business_logic.models.task import Task
from business_logic.models.velocity_trackable_task import VelocityTrackableTask


class VelocityTrackableTaskGetterProxy(TaskGetter[VelocityTrackableTask]):
    def __init__(self, task_getter: TaskGetter[Task]):
        self._task_getter = task_getter

    def get_task_by_id(self, task_id: str) -> Optional[VelocityTrackableTask]:
        task = self._task_getter.get_task_by_id(task_id)
        if task is not None and task.date_finished is not None:
            return self._to_velocity_trackable_task(task, task.date_finished)
        return None

    def get_tasks(self) -> List[VelocityTrackableTask]:
        return [
            self._to_velocity_trackable_task(task, task.date_finished)
            for task in self._flattened_tasks(self._task_getter.get_tasks())
            if task.date_finished is not None
        ]

    def _flattened_tasks(self, tasks: List[Task]) -> List[Task]:
        flattened_tasks: List[Task] = []
        for task in tasks:
            flattened_tasks = [
                *flattened_tasks,
                *self._flattened_tasks(task.sub_tasks),
                task,
            ]
        return flattened_tasks

    @staticmethod
    def _to_velocity_trackable_task(
        task: Task, date_finished: Date
    ) -> VelocityTrackableTask:
        return VelocityTrackableTask(
            id=task.id,
            story_points=task.story_points,
            assignees=task.assignees,
            date_started=task.date_started,
            date_finished=date_finished,
        )
