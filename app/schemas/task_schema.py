from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

class TaskUpdate(TaskBase):
    assignee_id: Optional[int] = None
    
class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
    priority: Optional[TaskPriority] = None
    skip: int = 0
    limit: int = 10
    sort_by: str = "created_at"
    sort_order: str = "desc"
    
class TaskStatusUpdate(BaseModel):
    new_status: TaskStatus

class TaskOut(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None

    class Config:
        orm_mode = True
