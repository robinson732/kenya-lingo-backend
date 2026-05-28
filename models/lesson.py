from extensions import db


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    episodeTitle = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    storyIntro = db.Column(db.Text, nullable=False)
    dialogue = db.Column(db.Text, nullable=False)
    exercises = db.Column(db.Text, nullable=False)
    xpReward = db.Column(db.Integer, default=10, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )

    questions = db.relationship(
        "Question",
        backref="lesson",
        lazy=True,
        cascade="all, delete-orphan",
    )
    dialogues = db.relationship(
        "Dialogue",
        backref="lesson",
        lazy=True,
        cascade="all, delete-orphan",
    )
    progress_entries = db.relationship(
        "UserProgress",
        backref="lesson",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Lesson {self.language} - {self.episodeTitle}>"

