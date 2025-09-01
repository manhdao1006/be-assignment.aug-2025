from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.schemas import user_schema
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.models.user import User, RoleEnum
from app.utils.jwt import verify_password, create_access_token, get_current_admin_user, get_password_hash

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=user_schema.UserOut)
def register(user_in: user_schema.UserRegister, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        user = user_service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
