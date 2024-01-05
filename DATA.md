# About The Data

## Developer Velocity

We take the median story points of all finished tasks per day to get the velocity for each developer.

To get the teams velocity we take the median story points of all developers in a team.

A task can have multiple developers assigned to it(e.g. PairProgramming or GroupProgramming).
For now, each developer assigned to a task will claim the same amount of story points, when a task is finished.

## Task Burn Down

The Task Burn Down Chart show the estimated time when a task will be finished by the team.
To calculate the burn down estimation for a single task we take the current velocity of the team per day and subtract
the velocity from the remaining story points each day until the task is done.

To get the Burn Down Metric for all the tasks we aggregate all the tasks remaining story points and estimate based on
the teams velocity.

The aggregated burn down will not show when individual tasks are done. However the estimated time will still be the time
all tasks are done since addition is associative.

## Developer Specific Dashboard

Each developer gets sees his/her own velocity and the teams velocity.
Each developer sees each current task and the estimation for his/her velocity and the teams to finish each task. 
