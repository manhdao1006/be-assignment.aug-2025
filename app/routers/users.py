from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import user_schema
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.utils.jwt import require_admin

router = APIRouter(tags=["Users"])

@router.post("/admin/add-user", response_model=user_schema.UserOut)
def add_user(
    user_in: user_schema.UserCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        user = user_service.add_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@router.put("/admin/edit-user/{user_id}", response_model=user_schema.UserOut)
def edit_user(
    user_id: int,
    user_in: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    user_service = UserService(UserRepository(db))
    try:
        updated_user = user_service.edit_user(
            user_id=user_id,
            user_in=user_in
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/admin/users")
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):
    user_service = UserService(UserRepository(db))
    result = user_service.get_all_users(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)
    return result

@router.get("/user/{user_id}", response_model=user_schema.UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_service = UserService(UserRepository(db))
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user-by-email", response_model=user_schema.UserOut)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    user_service = UserService(UserRepository(db))
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
