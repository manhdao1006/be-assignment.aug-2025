from sqlalchemy.orm import Session
from app.models.comment import Comment

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: Comment):
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_by_task(self, task_id: int):
        return (
            self.db.query(Comment)
            .filter(Comment.task_id == task_id, Comment.deleted_at.is_(None))
            .all()
        )

    def get_by_id(self, comment_id: int):
        return self.db.query(Comment).filter(Comment.id == comment_id, Comment.deleted_at.is_(None)).first()

    def update(self, comment: Comment):
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def soft_delete(self, comment: Comment):
        comment.is_deleted = True
        self.db.commit()
        self.db.refresh(comment)
        return comment
