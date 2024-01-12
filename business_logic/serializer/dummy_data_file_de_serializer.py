from typing import List

from pydantic import BaseModel

from business_logic.serializer.task import DeserializedTask

DeserializedTasks = List[DeserializedTask]


class DeserializedDummyTasksFile(BaseModel):
    tasks: DeserializedTasks
