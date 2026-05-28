from extensions import db


class UserQuestionAnswer(db.Model):
    __tablename__ = "user_question_answers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    xp_earned = db.Column(db.Integer, default=0, nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    answered_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "question_id", name="unique_user_question"),
    )

    def __repr__(self):
        return (
            f"<UserQuestionAnswer user_id={self.user_id} "
            f"question_id={self.question_id} xp_earned={self.xp_earned} "
            f"correct={self.correct}>"
        )
