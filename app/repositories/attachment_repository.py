from sqlalchemy.orm import Session
from app.models.attachment import Attachment
from datetime import datetime, timezone

class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, attachment: Attachment):
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment

    def get_by_task(self, task_id: int):
        return (
            self.db.query(Attachment)
            .filter(Attachment.task_id == task_id, Attachment.deleted_at.is_(None))
            .all()
        )

    def get(self, attachment_id: int):
        return (
            self.db.query(Attachment)
            .filter(Attachment.id == attachment_id, Attachment.deleted_at.is_(None))
            .first()
        )

    def soft_delete(self, attachment: Attachment):
        attachment.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        return attachment
