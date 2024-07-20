from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., example="Sample Task Title")
    description: Optional[str] = Field(None, example="Sample Task Description")
    completed: bool = Field(False, example=False)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInResponse(TaskBase):
    id: int
