from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.utils.jwt import get_current_user
from app.schemas import report_schema
from app.services.report_service import ReportService
from app.repositories.task_repository import TaskRepository

router = APIRouter(tags=["Reports"])

@router.get("/reports/{project_id}/task-count", response_model=report_schema.TaskStatusCount)
def get_task_count_by_status(
    project_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user),
):
    service = ReportService(TaskRepository(db))
    counts = service.get_task_count_by_status(project_id)
    return {"counts": counts}

@router.get("/reports/{project_id}/overdue-tasks", response_model=List[report_schema.OverdueTask])
def get_overdue_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user),
):
    service = ReportService(TaskRepository(db))
    return service.get_overdue_tasks(project_id)
