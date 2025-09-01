from app.repositories.task_repository import TaskRepository

class ReportService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def get_task_count_by_status(self, project_id: int):
        return self.task_repo.count_by_status(project_id)

    def get_overdue_tasks(self, project_id: int):
        return self.task_repo.get_overdue(project_id)
