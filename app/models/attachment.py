from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimeMixin, DeleteMixin

class Attachment(Base, TimeMixin, DeleteMixin):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task = relationship("Task", back_populates="attachments")
    user = relationship("User", back_populates="attachments")
