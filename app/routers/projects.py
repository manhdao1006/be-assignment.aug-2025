from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectOut
from app.schemas.user_schema import UserOut
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.services.project_service import ProjectService
from app.utils.jwt import require_admin_or_manager

router = APIRouter(tags=["Projects"])

@router.put("/admin/project/{project_id}/user/{user_id}", response_model=UserOut)
def add_user_to_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    project_service = ProjectService(ProjectRepository(db), UserRepository(db))
    try:
        return project_service.add_user_to_project(project_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/admin/project/{project_id}/user/{user_id}", response_model=UserOut)
def remove_user_from_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    project_service = ProjectService(ProjectRepository(db), UserRepository(db))
    try:
        return project_service.remove_user_from_project(project_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/projects")
def get_all_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    project_service = ProjectService(ProjectRepository(db))
    return project_service.get_all(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)

@router.get("/project/{project_id}", response_model=ProjectOut)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
):
    project_service = ProjectService(ProjectRepository(db))
    try:
        return project_service.get_by_id(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/admin/project", response_model=ProjectOut)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    project_service = ProjectService(ProjectRepository(db))
    return project_service.create(project_in)

@router.put("/admin/project/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    project_service = ProjectService(ProjectRepository(db))
    try:
        return project_service.update(project_id, project_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/admin/project/{project_id}", response_model=ProjectOut)
def soft_delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin_or_manager)
):
    project_service = ProjectService(ProjectRepository(db))
    try:
        return project_service.soft_delete(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
