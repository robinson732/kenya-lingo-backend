from extensions import db


class Dialogue(db.Model):
    __tablename__ = "dialogues"

    id = db.Column(db.Integer, primary_key=True)
    speaker = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)

    def __repr__(self):
        return f"<Dialogue {self.speaker}>"