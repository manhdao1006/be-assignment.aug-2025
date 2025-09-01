from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.services.task_service import TaskService
from app.utils.jwt import get_current_user, require_admin_or_manager
from app.models.task import TaskStatus, TaskPriority
from typing import Optional
from app.schemas.task_schema import TaskFilter, TaskStatusUpdate
from app.models.user import User

router = APIRouter(tags=["Tasks"])

@router.get("/project/{project_id}/tasks")
def list_tasks_in_project(
    project_id: int,
    status: Optional[TaskStatus] = Query(None),
    assignee_id: Optional[int] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    filters = TaskFilter(
        status=status,
        assignee_id=assignee_id,
        priority=priority,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return task_service.list_by_project(project_id, filters)

@router.put("/task/{task_id}/status", response_model=TaskOut)
def update_task_status_forward(
    task_id: int,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_user),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    try:
        return task_service.update_status_forward(task_id, status_update.new_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks")
def get_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    return task_service.get_all(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)

@router.get("/task/{task_id}", response_model=TaskOut)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    try:
        return task_service.get_by_id(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/projects/{project_id}/tasks", response_model=TaskOut)
def create_task(
    project_id: int,
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    try:
        return task_service.create(task_in, current_user, project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    try:
        return task_service.update(task_id, task_in, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/admin/task/{task_id}", response_model=TaskOut)
def soft_delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))
    try:
        return task_service.soft_delete(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
