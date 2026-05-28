from extensions import db
from datetime import date


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id"),
        nullable=False
    )

    xp = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

    completed_at = db.Column(
        db.Date,
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "lesson_id", name="unique_user_lesson"),
    )

    def add_xp(self, amount):
        self.xp += amount

    def mark_completed(self):
        self.completed = True
        self.completed_at = date.today()

    def __repr__(self):
        return (
            f"<UserProgress user_id={self.user_id} "
            f"lesson_id={self.lesson_id} "
            f"xp={self.xp} "
            f"completed={self.completed}>"
        )