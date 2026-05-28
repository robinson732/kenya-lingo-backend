from datetime import datetime, timezone
import uuid
from extensions import db


class EmailVerification(db.Model):
    __tablename__ = "email_verifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    token_type = db.Column(db.String(50), nullable=False)  # "verification" or "password_reset"
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="email_tokens")

    def __repr__(self):
        return f"<EmailVerification {self.token_type} for user_id={self.user_id}>"

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at

    def is_valid(self):
        return not self.is_used and not self.is_expired()