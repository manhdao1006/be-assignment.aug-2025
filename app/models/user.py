import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimeMixin, DeleteMixin

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"

class User(Base, TimeMixin, DeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="users")

    role = Column(Enum(RoleEnum), default=RoleEnum.MEMBER, nullable=False)

    projects = relationship("Project", secondary="project_members", back_populates="members")
    tasks = relationship("Task", back_populates="assignee")

    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
