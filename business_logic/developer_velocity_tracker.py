from typing import List

from business_logic.models.date import Date
from business_logic.models.developer_velocity import DeveloperVelocity
from business_logic.models.velocity_trackable_task import VelocityTrackableTask


class DeveloperVelocityTracker:
    def track_team_velocity(
        self, tasks: List[VelocityTrackableTask]
    ) -> DeveloperVelocity:
        team_velocity: DeveloperVelocity = {}
        for task in tasks:
            self.aggregate_velocity(
                a=team_velocity,
                b=self._distribute_story_points_among_days_between_start_and_end_date(
                    start_date=task.date_started,
                    end_date=task.date_finished,
                    story_points=task.story_points,
                ),
            )

        return team_velocity

    def track_average_developer_velocity(
        self, tasks: List[VelocityTrackableTask]
    ) -> DeveloperVelocity:
        number_of_contributing_developers = (
            self._get_number_of_total_contributing_developers(tasks)
        )
        team_velocity = self.track_team_velocity(tasks)
        return {
            date: story_points / number_of_contributing_developers
            for date, story_points in team_velocity.items()
        }

    @staticmethod
    def _get_number_of_total_contributing_developers(
        tasks: List[VelocityTrackableTask],
    ) -> int:
        contributing_developers = set()
        for task in tasks:
            for developer in task.assignees:
                contributing_developers.add(developer)
        return len(contributing_developers)

    def track_developer_velocity(
        self, tasks: List[VelocityTrackableTask], tracked_developer: str
    ) -> DeveloperVelocity:
        developer_velocity: DeveloperVelocity = {}
        for task in tasks:
            if tracked_developer in task.assignees:
                self.aggregate_velocity(
                    a=developer_velocity,
                    b=self._distribute_story_points_among_days_between_start_and_end_date(
                        start_date=task.date_started,
                        end_date=task.date_finished,
                        story_points=self._split_story_points_among_the_assignees(
                            story_points=task.story_points,
                            assignees=task.assignees,
                        ),
                    ),
                )
        return developer_velocity

    def aggregate_velocity(
        self, a: DeveloperVelocity, b: DeveloperVelocity
    ) -> DeveloperVelocity:
        for date, story_points in b.items():
            self._add_day_to_velocity(
                velocity=a, date=Date.from_string(date), story_points=story_points
            )
        return a

    @staticmethod
    def filter_velocity_for_given_start_date(
        velocity: DeveloperVelocity, start_date: Date
    ) -> DeveloperVelocity:
        return {
            date: story_points
            for date, story_points in velocity.items()
            if Date.from_string(date) >= start_date
        }

    @staticmethod
    def _add_day_to_velocity(
        velocity: DeveloperVelocity, date: Date, story_points: float
    ) -> DeveloperVelocity:
        if date.to_string() in velocity.keys():
            velocity[date.to_string()] += story_points
        else:
            velocity[date.to_string()] = story_points
        return velocity

    @staticmethod
    def _split_story_points_among_the_assignees(
        story_points: float, assignees: List[str]
    ) -> float:
        return story_points / len(assignees)

    @staticmethod
    def _distribute_story_points_among_days_between_start_and_end_date(
        start_date: Date, end_date: Date, story_points: float
    ) -> DeveloperVelocity:
        days_between_start_and_end_date = end_date.get_days_until(start_date)
        if days_between_start_and_end_date == 0:
            return {start_date.to_string(): story_points}
        # add one day, if 1 day is between 2 days we have to divide the story points by 2
        adjusted_days_between_the_dates_to_divide_by = (
            days_between_start_and_end_date + 1
        )
        story_points_per_day = (
            story_points / adjusted_days_between_the_dates_to_divide_by
        )
        if days_between_start_and_end_date == 1:
            return {
                start_date.to_string(): story_points_per_day,
                end_date.to_string(): story_points_per_day,
            }
        if days_between_start_and_end_date > 1:
            developer_velocity: DeveloperVelocity = {}
            for days in range(0, days_between_start_and_end_date + 1):
                date = start_date.add_days(days)
                developer_velocity = {
                    **developer_velocity,
                    date.to_string(): story_points_per_day,
                }
            return developer_velocity
        return {}
