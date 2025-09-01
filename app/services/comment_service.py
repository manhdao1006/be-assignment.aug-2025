from app.repositories.comment_repository import CommentRepository
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.models.comment import Comment
from app.models.user import User
from datetime import datetime

class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    def create(self, comment_in: CommentCreate, current_user: User):
        comment = Comment(
            content=comment_in.content,
            task_id=comment_in.task_id,
            user_id=current_user.id,
        )
        return self.repo.create(comment)

    def list_by_task(self, task_id: int):
        return self.repo.get_by_task(task_id)

    def update(self, comment_id: int, comment_in: CommentUpdate, current_user: User):
        comment = self.repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != current_user.id:
            raise ValueError("Not allowed to edit this comment")
        comment.content = comment_in.content
        return self.repo.update(comment)

    def soft_delete(self, comment_id: int, current_user: User):
        comment = self.repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != current_user.id:
            raise ValueError("Not allowed to delete this comment")
        return self.repo.soft_delete(comment)