from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class CommentUpdate(BaseModel):
    content: str

class CommentOut(CommentBase):
    id: int
    user_id: int
    task_id: int
    created_at: datetime

    class Config:
        orm_mode = True
