from extensions import db
import json

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=True)  # JSON string of answer options
    xp = db.Column(db.Integer, default=5)

    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)

    def get_options(self):
        """Parse options from JSON string"""
        if self.options:
            try:
                return json.loads(self.options)
            except json.JSONDecodeError:
                return None
        return None

    def set_options(self, options_list):
        """Convert options list to JSON string"""
        if options_list:
            self.options = json.dumps(options_list)

    def __repr__(self):
        return f"<Question {self.prompt}>"