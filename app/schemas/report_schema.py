from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class TaskStatusCount(BaseModel):
    counts: Dict[str, int]

class OverdueTask(BaseModel):
    id: int
    title: str
    due_date: datetime
    status: str

    class Config:
        orm_mode = True
