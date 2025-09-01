from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import user_schema
from app.schemas.organization_schema import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.organization_service import OrganizationService
from app.utils.jwt import require_admin

router = APIRouter(tags=["Organizations"])

@router.put("/admin/org/{org_id}/user/{user_id}", response_model=user_schema.UserOut)
def add_user_to_org(
    org_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    org_service = OrganizationService(
        OrganizationRepository(db),
        UserRepository(db)
    )
    try:
        updated_user = org_service.add_user_to_org(user_id, org_id)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orgs")
def get_all_orgs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    org_service = OrganizationService(OrganizationRepository(db))
    return org_service.get_all(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)

@router.get("/org/{org_id}", response_model=OrganizationOut)
def get_org_by_id(
    org_id: int,
    db: Session = Depends(get_db),
):
    org_service = OrganizationService(OrganizationRepository(db))
    try:
        return org_service.get_by_id(org_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/admin/org", response_model=OrganizationOut)
def create_org(
    org_in: OrganizationCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    org_service = OrganizationService(OrganizationRepository(db))
    return org_service.create(org_in)

@router.put("/admin/org/{org_id}", response_model=OrganizationOut)
def update_org(
    org_id: int,
    org_in: OrganizationUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    org_service = OrganizationService(OrganizationRepository(db))
    try:
        return org_service.update(org_id, org_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/admin/org/{org_id}", response_model=OrganizationOut)
def soft_delete_org(
    org_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    org_service = OrganizationService(OrganizationRepository(db))
    try:
        return org_service.soft_delete(org_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

