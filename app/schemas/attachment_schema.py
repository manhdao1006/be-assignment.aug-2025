from pydantic import BaseModel
from datetime import datetime

class AttachmentBase(BaseModel):
    file_path: str
    file_name: str

class AttachmentOut(AttachmentBase):
    id: int
    user_id: int
    task_id: int
    created_at: datetime

    class Config:
        orm_mode = True
