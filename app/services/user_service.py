from app.repositories.user_repository import UserRepository
from app.models.user import User, RoleEnum
from app.utils.jwt import get_password_hash

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_in):
        if self.user_repo.get_by_email(user_in.email):
            raise ValueError("Email already registered")
        hashed_pw = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            password=hashed_pw,
            full_name=user_in.full_name,
            role=user_in.role or RoleEnum.MEMBER,
        )
        return self.user_repo.create(user)

    def add_user(self, user_in):
        if self.user_repo.get_by_email(user_in.email):
            raise ValueError("Email already registered")
        hashed_pw = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            password=hashed_pw,
            full_name=user_in.full_name,
            role=user_in.role or RoleEnum.MEMBER,
            organization_id=user_in.organization_id or None
        )
        return self.user_repo.create(user)
    
    def edit_user(self, user_id: int, user_in):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User does not exist")

        if user_in.organization_id:
            user.organization_id = user_in.organization_id

        if user_in.full_name:
            user.full_name = user_in.full_name
        if user_in.role:
            user.role = user_in.role

        return self.user_repo.update(user)

    def get_all_users(self, skip: int = 0, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
        if not hasattr(User, sort_by):
            sort_by = "id"
        column = getattr(User, sort_by)
        order_by = column.desc() if sort_order == "desc" else column.asc()
        users = self.user_repo.get_all(skip=skip, limit=limit, order_by=order_by)
        total = self.user_repo.count()
        pagination = {
            "total": total,
            "skip": skip,
            "limit": limit,
            "returned": len(users)
        }
        return {"pagination": pagination, "users": users}

    def get_user_by_id(self, user_id: int):
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_email(email)