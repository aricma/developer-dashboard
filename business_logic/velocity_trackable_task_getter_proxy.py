from typing import List

from business_logic.interfaces.task_getter import TaskGetter
from business_logic.models.task import Task
from business_logic.models.velocity_trackable_task import VelocityTrackableTask


class VelocityTrackableTaskGetterProxy(TaskGetter[VelocityTrackableTask]):
    def __init__(self, task_getter: TaskGetter[Task]):
        self._task_getter = task_getter

    def get_tasks(self) -> List[VelocityTrackableTask]:
        return [
            self._to_velocity_trackable_task(task)
            for task in self._flattened_tasks(self._task_getter.get_tasks())
            if task.date_finished is not None
        ]

    def _flattened_tasks(self, tasks: List[Task]) -> List[Task]:
        flattened_tasks = []
        for task in tasks:
            flattened_tasks = [
                *flattened_tasks,
                *self._flattened_tasks(task.sub_tasks),
                task,
            ]
        return flattened_tasks

    @staticmethod
    def _to_velocity_trackable_task(task: Task) -> VelocityTrackableTask:
        return VelocityTrackableTask(
            id=task.id,
            story_points=task.story_points,
            assignees=task.assignees,
            date_started=task.date_started,
            date_finished=task.date_finished,
        )
