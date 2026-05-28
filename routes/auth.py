from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import uuid

from models.email import EmailVerification, db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
mail = Mail()


# ─── REGISTER ────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        is_verified=False
    )
    db.session.add(user)
    db.session.flush()  # get user.id before committing

    # create verification token
    token = EmailVerification(
        user_id=user.id,
        token=str(uuid.uuid4()),
        token_type="verification",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
    )
    db.session.add(token)
    db.session.commit()

    # send verification email
    _send_verification_email(user.email, token.token)

    return jsonify({"message": "Registration successful. Please check your email to verify your account."}), 201


# ─── VERIFY EMAIL ─────────────────────────────────────────────────────────────

@auth_bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    record = EmailVerification.query.filter_by(token=token, token_type="verification").first()

    if not record:
        return jsonify({"error": "Invalid token"}), 404

    if not record.is_valid():
        return jsonify({"error": "Token has expired or already been used"}), 400

    record.is_used = True
    record.user.is_verified = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully. You can now log in."}), 200


# ─── LOGIN ────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_verified:
        return jsonify({"error": "Please verify your email before logging in"}), 403

    # TODO: return JWT token here later
    return jsonify({"message": "Login successful", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200


# ─── FORGOT PASSWORD ──────────────────────────────────────────────────────────

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    # always return 200 so we don't reveal if email exists
    if not user:
        return jsonify({"message": "If that email exists, a reset link has been sent"}), 200

    token = EmailVerification(
        user_id=user.id,
        token=str(uuid.uuid4()),
        token_type="password_reset",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    db.session.add(token)
    db.session.commit()

    _send_password_reset_email(user.email, token.token)

    return jsonify({"message": "If that email exists, a reset link has been sent"}), 200


# ─── RESET PASSWORD ───────────────────────────────────────────────────────────

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    record = EmailVerification.query.filter_by(token=token, token_type="password_reset").first()

    if not record:
        return jsonify({"error": "Invalid token"}), 404

    if not record.is_valid():
        return jsonify({"error": "Token has expired or already been used"}), 400

    record.user.password_hash = generate_password_hash(new_password)
    record.is_used = True
    db.session.commit()

    return jsonify({"message": "Password reset successful. You can now log in."}), 200


# ─── EMAIL HELPERS ────────────────────────────────────────────────────────────

def _send_verification_email(to_email, token):
    verify_url = f"http://localhost:5000/api/auth/verify-email/{token}"
    msg = Message(
        subject="Verify your Kenya Lingo account",
        recipients=[to_email],
        body=f"Welcome to Kenya Lingo!\n\nPlease verify your email by clicking the link below:\n\n{verify_url}\n\nThis link expires in 24 hours."
    )
    mail.send(msg)


def _send_password_reset_email(to_email, token):
    reset_url = f"http://localhost:5000/api/auth/reset-password?token={token}"
    msg = Message(
        subject="Reset your Kenya Lingo password",
        recipients=[to_email],
        body=f"You requested a password reset for your Kenya Lingo account.\n\nClick the link below to reset your password:\n\n{reset_url}\n\nThis link expires in 1 hour.\n\nIf you did not request this, please ignore this email."
    )
    mail.send(msg)