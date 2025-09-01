from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import comment_schema
from app.services.comment_service import CommentService
from app.repositories.comment_repository import CommentRepository
from app.utils.jwt import get_current_user
from app.models.user import User

router = APIRouter(tags=["Comments"])

@router.post("/comment/", response_model=comment_schema.CommentOut)
def create_comment(
    comment_in: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CommentService(CommentRepository(db))
    try:
        return service.create(comment_in, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comment/task/{task_id}", response_model=List[comment_schema.CommentOut])
def list_comments(
    task_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user)
):
    service = CommentService(CommentRepository(db))
    return service.list_by_task(task_id)

@router.put("/comment/{comment_id}", response_model=comment_schema.CommentOut)
def update_comment(
    comment_id: int,
    comment_in: comment_schema.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CommentService(CommentRepository(db))
    try:
        return service.update(comment_id, comment_in, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/comment/{comment_id}", response_model=comment_schema.CommentOut)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CommentService(CommentRepository(db))
    try:
        return service.soft_delete(comment_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
