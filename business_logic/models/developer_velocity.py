from typing import Dict

from business_logic.models.types import StoryPoints
from domain_models.task import Date

DeveloperVelocity = Dict[Date, StoryPoints]
