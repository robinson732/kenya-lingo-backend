from extensions import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_active = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    progress = db.relationship("UserProgress", backref="user", lazy=True, cascade="all, delete-orphan")
    email_tokens = db.relationship(
        "EmailVerification",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    # -------------------------
    # Password Methods
    # -------------------------

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # -------------------------
    # XP Logic
    # -------------------------

    def add_xp(self, amount):
        self.xp += amount

    # -------------------------
    # Streak Logic
    # -------------------------

    def update_streak(self):
        today = date.today()

        if self.last_active is None:
            self.streak = 1
        else:
            diff = (today - self.last_active).days

            if diff == 1:
                self.streak += 1
            elif diff > 1:
                self.streak = 1
            # if diff == 0 → same day, streak unchanged

        self.last_active = today

    def __repr__(self):
        return f"<User {self.name} | XP: {self.xp} | Streak: {self.streak}>"