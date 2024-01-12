from datetime import timedelta as duration

from dateutil.parser import parse as to_date
from typing import Dict, List

from business_logic.models import StoryPoints
from domain_models.task import FinishedTask, Date

from business_logic.models.developer_velocity import DeveloperVelocity


class DeveloperVelocityTracker:

    def track_team_velocity(self, tasks: List[FinishedTask]) -> Velocity:
        team_velocity: Velocity = {}
        for task in tasks:
            self.aggregate_velocity(
                a=team_velocity,
                b=self._distribute_story_points_among_days_between_start_and_end_date(
                    start_date=task.date_started,
                    end_date=task.date_finished,
                    story_points=task.story_points
                )
            )

        return team_velocity

    def track_average_developer_velocity(self, tasks: List[FinishedTask]) -> Velocity:
        number_of_contributing_developers = self._get_number_of_total_contributing_developers(tasks)
        team_velocity = self.track_team_velocity(tasks)
        return {
            date: story_points / number_of_contributing_developers
            for date, story_points in team_velocity.items()
        }

    @staticmethod
    def _get_number_of_total_contributing_developers(tasks: List[FinishedTask]) -> int:
        contributing_developers = set()
        for task in tasks:
            for developer in task.assignees:
                contributing_developers.add(developer)
        return len(contributing_developers)

    def track_developer_velocity(self, tasks: List[FinishedTask], tracked_developer: str) -> Velocity:
        developer_velocity: Velocity = {}
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
                        )
                    )
                )
        return developer_velocity

    def aggregate_velocity(self, a: Velocity, b: Velocity) -> Velocity:
        for date, story_points in b.items():
            self._add_day_to_velocity(
                velocity=a,
                date=date,
                story_points=story_points
            )
        return a

    @staticmethod
    def filter_velocity_for_given_start_date(velocity: Velocity, start_date: str) -> Velocity:
        return {
            date: story_points
            for date, story_points in velocity.items()
            if to_date(date) >= to_date(start_date)
        }

    @staticmethod
    def _add_day_to_velocity(velocity: Velocity, date: str, story_points: float) -> Velocity:
        if date in velocity.keys():
            velocity[date] += story_points
        else:
            velocity[date] = story_points
        return velocity

    @staticmethod
    def _split_story_points_among_the_assignees(story_points: float, assignees: List[str]) -> float:
        return story_points / len(assignees)

    @staticmethod
    def _distribute_story_points_among_days_between_start_and_end_date(
            start_date: str, end_date: str, story_points: float
    ) -> Velocity:
        days_between_start_and_end_date = (to_date(end_date) - to_date(start_date)).days
        if days_between_start_and_end_date == 0:
            return {
                start_date: story_points
            }
        # add one day, if 1 day is between 2 days we have to divide the story points by 2
        adjusted_days_between_the_dates_to_divide_by = days_between_start_and_end_date + 1
        story_points_per_day = story_points / adjusted_days_between_the_dates_to_divide_by
        if days_between_start_and_end_date == 1:
            return {
                start_date: story_points_per_day,
                end_date: story_points_per_day,
            }
        if days_between_start_and_end_date > 1:
            developer_velocity: Velocity = {}
            for days in range(0, days_between_start_and_end_date + 1):
                date = str(to_date(start_date) + duration(days=days))
                developer_velocity = {
                    **developer_velocity,
                    date: story_points_per_day
                }
            return developer_velocity
        return {}
