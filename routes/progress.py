from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Lesson, Question, UserProgress, UserQuestionAnswer
from datetime import date

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")


def _serialize_progress(progress: UserProgress):
    return {
        "id": progress.id,
        "user_id": progress.user_id,
        "lesson_id": progress.lesson_id,
        "xp": progress.xp,
        "completed": progress.completed,
        "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
    }


def _get_or_create_progress(user_id: int, lesson_id: int) -> UserProgress:
    progress = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            xp=0,
            completed=False,
            completed_at=None,
        )
        db.session.add(progress)
    return progress


@progress_bp.route("/lesson/<int:lesson_id>/answer", methods=["POST"])
def answer_question(lesson_id):
    data = request.get_json() or {}
    user_id = data.get("user_id")
    question_id = data.get("question_id")
    answer = data.get("answer")

    if not user_id or not question_id or answer is None:
        return jsonify({"error": "user_id, question_id, and answer are required"}), 400

    user = User.query.get(user_id)
    lesson = Lesson.query.get(lesson_id)
    question = Question.query.get(question_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    if not question or question.lesson_id != lesson_id:
        return jsonify({"error": "Question not found for this lesson"}), 404

    normalized_answer = str(answer).strip().lower()
    expected_answer = str(question.answer).strip().lower()
    if normalized_answer != expected_answer:
        progress = _get_or_create_progress(user_id, lesson_id)
        db.session.commit()
        return jsonify({
            "message": "Incorrect answer",
            "correct": False,
            "xpEarned": 0,
            "lessonXp": progress.xp,
            "totalXp": user.xp,
            "progress": _serialize_progress(progress),
        }), 200

    existing_answer = UserQuestionAnswer.query.filter_by(
        user_id=user_id,
        question_id=question_id,
    ).first()
    if existing_answer:
        progress = _get_or_create_progress(user_id, lesson_id)
        db.session.commit()
        return jsonify({
            "message": "Question already answered",
            "correct": True,
            "xpEarned": 0,
            "lessonXp": progress.xp,
            "totalXp": user.xp,
            "progress": _serialize_progress(progress),
        }), 200

    progress = _get_or_create_progress(user_id, lesson_id)
    answer_record = UserQuestionAnswer(
        user_id=user_id,
        question_id=question_id,
        lesson_id=lesson_id,
        xp_earned=question.xp,
        correct=True,
    )
    progress.add_xp(question.xp)
    user.add_xp(question.xp)
    db.session.add(answer_record)
    db.session.commit()

    return jsonify({
        "message": "Correct answer",
        "correct": True,
        "xpEarned": question.xp,
        "lessonXp": progress.xp,
        "totalXp": user.xp,
        "progress": _serialize_progress(progress),
    }), 200


@progress_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_progress(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    progress_entries = UserProgress.query.filter_by(user_id=user_id).all()
    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "total_xp": user.xp,
        "streak": user.streak,
        "progress": [_serialize_progress(p) for p in progress_entries],
    }), 200


@progress_bp.route("/lesson/<int:lesson_id>/complete", methods=["POST"])
def complete_lesson(lesson_id):
    data = request.get_json() or {}
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(user_id)
    lesson = Lesson.query.get(lesson_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404

    progress = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            xp=0,
            completed=False,
            completed_at=None,
        )
        db.session.add(progress)

    if progress.completed:
        return jsonify({
            "message": "Lesson already completed",
            "xpEarned": 0,
            "lessonXp": progress.xp,
            "totalXp": user.xp,
            "progress": _serialize_progress(progress),
        }), 200

    progress.mark_completed()
    db.session.commit()

    return jsonify({
        "message": "Lesson completed",
        "xpEarned": 0,
        "lessonXp": progress.xp,
        "totalXp": user.xp,
        "progress": _serialize_progress(progress),
    }), 200
