from typing import Dict, Union

from business_logic.models.story_points import StoryPoints, EstimatedStoryPoints

Date = str

BurnDownForecast = Dict[Date, Union[StoryPoints, EstimatedStoryPoints]]
