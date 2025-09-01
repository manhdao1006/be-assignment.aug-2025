import os
from fastapi import UploadFile
from app.models.attachment import Attachment
from app.models.user import User
from app.repositories.attachment_repository import AttachmentRepository

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_ATTACHMENTS_PER_TASK = 3

class AttachmentService:
    def __init__(self, repo: AttachmentRepository):
        self.repo = repo

    def upload(self, task_id: int, file: UploadFile, current_user: User):
        attachments = self.repo.get_by_task(task_id)
        if len(attachments) >= MAX_ATTACHMENTS_PER_TASK:
            raise ValueError("Attachments limited to max 3 per task")

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise ValueError("Attachments limited to 5MB each")
        
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        unique_name = f"{current_user.id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        attachment = Attachment(
            file_name=file.filename,
            file_path=file_path,
            task_id=task_id,
            user_id=current_user.id,
        )
        return self.repo.create(attachment)

    def list_by_task(self, task_id: int):
        return self.repo.get_by_task(task_id)
    
    def get(self, attachment_id: int, current_user: User):
        attachment = self.repo.get(attachment_id)
        if not attachment:
            return None
        if attachment.user_id != current_user.id:
            return None
        return attachment

    def delete(self, attachment_id: int, current_user: User):
        attachment = self.repo.get(attachment_id)
        if not attachment:
            raise ValueError("Attachment not found")
        if attachment.user_id != current_user.id:
            raise ValueError("Not allowed to delete this attachment")

        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)

        return self.repo.soft_delete(attachment)
