from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from app.models.task import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_by_status(self, project_id: int):
        result = (
            self.db.query(Task.status, func.count(Task.id))
            .filter(Task.project_id == project_id, Task.deleted_at.is_(None))
            .group_by(Task.status)
            .all()
        )
        return {status.value: count for status, count in result}

    def get_overdue(self, project_id: int):
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.due_date != None,
                Task.due_date < now,
                Task.deleted_at.is_(None)
            )
            .all()
        )

    def get_by_project(
        self,
        project_id: int,
        status=None,
        assignee_id=None,
        priority=None,
        skip: int = 0,
        limit: int = 10,
        order_by=None
    ):
        query = self.db.query(Task).filter(Task.project_id == project_id, Task.deleted_at.is_(None))

        if status:
            query = query.filter(Task.status == status)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if priority:
            query = query.filter(Task.priority == priority)

        if order_by is not None:
            query = query.order_by(order_by)

        return query.offset(skip).limit(limit).all()

    def count_by_project(self, project_id: int, status=None, assignee_id=None, priority=None):
        query = self.db.query(Task).filter(Task.project_id == project_id, Task.deleted_at.is_(None))

        if status:
            query = query.filter(Task.status == status)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if priority:
            query = query.filter(Task.priority == priority)

        return query.count()

    def get_all(self, skip: int = 0, limit: int = 10, order_by=None):
        query = self.db.query(Task).filter(Task.is_deleted == False)
        if order_by is not None:
            query = query.order_by(order_by)
        return query.offset(skip).limit(limit).all()

    def count(self):
        return self.db.query(Task).filter(Task.is_deleted == False).count()

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()

    def create(self, task: Task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def soft_delete(self, task: Task):
        task.is_deleted = True
        self.db.commit()
        self.db.refresh(task)
        return task
