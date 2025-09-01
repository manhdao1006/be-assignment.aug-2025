from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10, order_by=None):
        query = self.db.query(Project).filter(Project.is_deleted == False)
        if order_by is not None:
            query = query.order_by(order_by)
        return query.offset(skip).limit(limit).all()

    def count(self):
        return self.db.query(Project).filter(Project.is_deleted == False).count()

    def get_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id, Project.is_deleted == False).first()

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project):
        self.db.commit()
        self.db.refresh(project)
        return project

    def soft_delete(self, project: Project):
        project.is_deleted = True
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def add_user(self, project: Project, user: User):
        if user not in project.members:
            project.members.append(user)
            self.db.commit()
            self.db.refresh(project)
        return user

    def remove_user(self, project: Project, user: User):
        if user in project.members:
            project.members.remove(user)
            self.db.commit()
            self.db.refresh(project)
        return user
