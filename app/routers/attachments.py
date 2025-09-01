from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas import attachment_schema
from app.services.attachment_service import AttachmentService
from app.repositories.attachment_repository import AttachmentRepository
from app.utils.jwt import get_current_user
from fastapi.responses import FileResponse

router = APIRouter(tags=["Attachments"])

@router.post("/attachments/{task_id}", response_model=attachment_schema.AttachmentOut)
def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AttachmentService(AttachmentRepository(db))
    try:
        return service.upload(task_id, file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/attachments/{task_id}", response_model=List[attachment_schema.AttachmentOut])
def list_attachments(
    task_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user),
):
    service = AttachmentService(AttachmentRepository(db))
    return service.list_by_task(task_id)

@router.delete("/attachments/{attachment_id}", response_model=attachment_schema.AttachmentOut)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AttachmentService(AttachmentRepository(db))
    try:
        return service.delete(attachment_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/attachments/download/{attachment_id}")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AttachmentService(AttachmentRepository(db))
    attachment = service.get(attachment_id, current_user)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return FileResponse(
        path=attachment.file_path,
        filename=attachment.file_name,
        media_type="application/octet-stream",
    )
