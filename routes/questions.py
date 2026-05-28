from flask import Blueprint, request, jsonify
from extensions import db
from models.question import Question
from models.lesson import Lesson

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


@questions_bp.route("/", methods=["GET"])
def list_questions():
    questions = Question.query.all()
    output = []
    for q in questions:
        output.append({
            "id": q.id,
            "question_type": q.question_type,
            "prompt": q.prompt,
            "answer": q.answer,
            "options": q.get_options(),
            "xp": q.xp,
            "lesson_id": q.lesson_id,
        })
    return jsonify(output), 200


@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_question(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({
        "id": q.id,
        "question_type": q.question_type,
        "prompt": q.prompt,
        "answer": q.answer,
        "options": q.get_options(),
        "xp": q.xp,
        "lesson_id": q.lesson_id,
    }), 200


@questions_bp.route("/lesson/<int:lesson_id>", methods=["GET"])
def questions_by_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    output = [
        {
            "id": q.id,
            "question_type": q.question_type,
            "prompt": q.prompt,
            "answer": q.answer,
            "options": q.get_options(),
            "xp": q.xp,
            "lesson_id": q.lesson_id,
        }
        for q in questions
    ]
    return jsonify(output), 200


@questions_bp.route("/", methods=["POST"])
def create_question():
    data = request.get_json() or {}
    required = ["question_type", "prompt", "answer", "lesson_id"]
    for f in required:
        if f not in data:
            return jsonify({"error": f"{f} is required"}), 400

    # verify lesson exists
    if not Lesson.query.get(data["lesson_id"]):
        return jsonify({"error": "Associated lesson not found"}), 404

    q = Question(
        question_type=data["question_type"],
        prompt=data["prompt"],
        answer=data["answer"],
        xp=data.get("xp", 5),
        lesson_id=data["lesson_id"],
    )
    if "options" in data:
        q.set_options(data["options"])
    db.session.add(q)
    db.session.commit()
    return jsonify({"message": "Question created", "id": q.id}), 201


@questions_bp.route("/<int:question_id>", methods=["PUT", "PATCH"])
def update_question(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404
    data = request.get_json() or {}
    for key in ["question_type", "prompt", "answer", "xp", "lesson_id"]:
        if key in data:
            setattr(q, key, data[key])
    if "options" in data:
        q.set_options(data["options"])
    db.session.commit()
    return jsonify({"message": "Question updated"}), 200


@questions_bp.route("/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404
    db.session.delete(q)
    db.session.commit()
    return jsonify({"message": "Question deleted"}), 200
