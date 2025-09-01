from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.models.project import Project

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository = None):
        self.project_repo = project_repo
        self.user_repo = user_repo

    def get_all(self, skip: int = 0, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
        if not hasattr(Project, sort_by):
            sort_by = "id"
        column = getattr(Project, sort_by)
        order_by = column.desc() if sort_order == "desc" else column.asc()
        projects = self.project_repo.get_all(skip=skip, limit=limit, order_by=order_by)
        total = self.project_repo.count()
        pagination = {
            "total": total,
            "skip": skip,
            "limit": limit,
            "returned": len(projects)
        }
        return {"pagination": pagination, "projects": projects}

    def get_by_id(self, project_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        return project

    def create(self, project_in):
        project = Project(
            name=project_in.name,
            description=project_in.description,
            organization_id=project_in.organization_id
        )
        return self.project_repo.create(project)

    def update(self, project_id: int, project_in):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        project.name = project_in.name
        project.description = project_in.description
        return self.project_repo.update(project)

    def soft_delete(self, project_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        return self.project_repo.soft_delete(project)
    
    def add_user_to_project(self, project_id: int, user_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return self.project_repo.add_user(project, user)

    def remove_user_from_project(self, project_id: int, user_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return self.project_repo.remove_user(project, user)
