from app.repositories.task_repository import TaskRepository
from app.models.task import Task, TaskStatus
from app.schemas.task_schema import TaskFilter
from datetime import datetime,  timezone
from app.models.user import RoleEnum
from app.repositories.project_repository import ProjectRepository

class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def _validate_due_date(self, due_date):
        now_utc = datetime.now(timezone.utc)
        if due_date and due_date < now_utc:
            raise ValueError("Due date must be today or in the future")

    def _validate_membership(self, project, current_user):
        if current_user.role in ["admin", "manager"]:
            return

        if current_user not in project.members:
            raise ValueError("Only project members can perform this action")

    def _validate_assignment(self, project, current_user, assignee_id):
        if not assignee_id:
            return

        if current_user.role in [RoleEnum.ADMIN, RoleEnum.MANAGER]:
            assignee = next((m for m in project.members if m.id == assignee_id), None)
            if not assignee:
                raise ValueError("Assignee must be a project member")
        else:
            if assignee_id != current_user.id:
                raise ValueError("Members can only assign tasks to themselves")

    def list_by_project(self, project_id: int, filters: TaskFilter):
        if not hasattr(Task, filters.sort_by):
            filters.sort_by = "id"
        column = getattr(Task, filters.sort_by)
        order_by = column.desc() if filters.sort_order == "desc" else column.asc()

        tasks = self.task_repo.get_by_project(
            project_id=project_id,
            status=filters.status,
            assignee_id=filters.assignee_id,
            priority=filters.priority,
            skip=filters.skip,
            limit=filters.limit,
            order_by=order_by
        )
        total = self.task_repo.count_by_project(
            project_id=project_id,
            status=filters.status,
            assignee_id=filters.assignee_id,
            priority=filters.priority
        )

        pagination = {
            "total": total,
            "skip": filters.skip,
            "limit": filters.limit,
            "returned": len(tasks)
        }
        return {"pagination": pagination, "tasks": tasks}

    def update_status_forward(self, task_id: int, new_status: TaskStatus):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        allowed_transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
            TaskStatus.DONE: []
        }

        if new_status not in allowed_transitions[task.status]:
            raise ValueError(f"Invalid transition: {task.status.value} → {new_status.value}")

        task.status = new_status
        return self.task_repo.update(task)

    def get_all(self, skip: int = 0, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
        if not hasattr(Task, sort_by):
            sort_by = "id"
        column = getattr(Task, sort_by)
        order_by = column.desc() if sort_order == "desc" else column.asc()

        tasks = self.task_repo.get_all(skip=skip, limit=limit, order_by=order_by)
        total = self.task_repo.count()
        pagination = {
            "total": total,
            "skip": skip,
            "limit": limit,
            "returned": len(tasks)
        }
        return {"pagination": pagination, "tasks": tasks}

    def get_by_id(self, task_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    def create(self, task_in, current_user, project_id: int):
        project = self.project_repo.get_by_id(task_in.project_id)
        if not project:
            raise ValueError("Project not found")

        self._validate_membership(project, current_user)
        self._validate_due_date(task_in.due_date)
        self._validate_assignment(project, current_user, task_in.assignee_id)

        task = Task(
            title=task_in.title,
            description=task_in.description,
            status=TaskStatus.TODO,
            priority=task_in.priority,
            due_date=task_in.due_date,
            project_id=project_id,
            assignee_id=task_in.assignee_id,
        )
        return self.task_repo.create(task)

    def update(self, task_id: int, task_in, current_user):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        project = task.project
        self._validate_membership(project, current_user)
        self._validate_due_date(task_in.due_date)
        self._validate_assignment(project, current_user, task_in.assignee_id)

        task.title = task_in.title
        task.description = task_in.description
        task.status = task_in.status
        task.priority = task_in.priority
        task.due_date = task_in.due_date
        task.assignee_id = task_in.assignee_id

        return self.task_repo.update(task)

    def soft_delete(self, task_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return self.task_repo.soft_delete(task)
