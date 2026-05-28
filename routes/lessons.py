from flask import Blueprint, request, jsonify
from extensions import db
from models.lesson import Lesson
from models.question import Question

lessons_bp = Blueprint("lessons", __name__, url_prefix="/api/lessons")


# helper serializer

def _lesson_to_dict(lesson: Lesson):
    return {
        "id": lesson.id,
        "language": lesson.language,
        "episodeTitle": lesson.episodeTitle,
        "difficulty": lesson.difficulty,
        "storyIntro": lesson.storyIntro,
        "dialogue": lesson.dialogue,
        "exercises": lesson.exercises,
        "xpReward": lesson.xpReward,
    }


@lessons_bp.route("/", methods=["GET"])
def list_lessons():
    lessons = Lesson.query.all()
    return jsonify([_lesson_to_dict(l) for l in lessons]), 200


@lessons_bp.route("/<int:lesson_id>", methods=["GET"])
def get_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(_lesson_to_dict(lesson)), 200


@lessons_bp.route("/", methods=["POST"])
def create_lesson():
    data = request.get_json() or {}
    required = [
        "language",
        "episodeTitle",
        "difficulty",
        "storyIntro",
        "dialogue",
        "exercises",
        "xpReward",
    ]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    lesson = Lesson(
        language=data["language"],
        episodeTitle=data["episodeTitle"],
        difficulty=data["difficulty"],
        storyIntro=data["storyIntro"],
        dialogue=data["dialogue"],
        exercises=data["exercises"],
        xpReward=data["xpReward"],
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson created", "id": lesson.id}), 201


@lessons_bp.route("/<int:lesson_id>", methods=["PUT", "PATCH"])
def update_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404

    data = request.get_json() or {}
    # update only provided fields
    for key in [
        "language",
        "episodeTitle",
        "difficulty",
        "storyIntro",
        "dialogue",
        "exercises",
        "xpReward",
    ]:
        if key in data:
            setattr(lesson, key, data[key])

    db.session.commit()
    return jsonify({"message": "Lesson updated"}), 200


@lessons_bp.route("/<int:lesson_id>", methods=["DELETE"])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson deleted"}), 200


# nested resource: questions for a lesson
@lessons_bp.route("/<int:lesson_id>/questions", methods=["GET"])
def get_lesson_questions(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    output = []
    for q in questions:
        output.append({
            "id": q.id,
            "question_type": q.question_type,
            "prompt": q.prompt,
            "answer": q.answer,
            "xp": q.xp,
            "lesson_id": q.lesson_id,
        })
    return jsonify(output), 200
