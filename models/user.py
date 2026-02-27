from extensions import db
from datetime import date

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # for login
    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_active = db.Column(db.Date, default=date.today, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    progress = db.relationship("UserProgress", backref="user", lazy=True)

    # Methods
    def add_xp(self, amount):
        self.xp += amount

    def update_streak(self):
        today = date.today()
        if self.last_active is None:
            self.streak = 1
        else:
            diff = (today - self.last_active).days
            self.streak = self.streak + 1 if diff == 1 else 1
        self.last_active = today
