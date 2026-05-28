import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models.lesson import Lesson
from models.question import Question
from models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    # use in-memory database for tests
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_lesson_crud(client):
    # create new lesson
    payload = {
        "language": "luo",
        "episodeTitle": "Episode 1",
        "difficulty": "easy",
        "storyIntro": "Once upon a time...",
        "dialogue": "Hello",
        "exercises": "translate",
        "xpReward": 10,
    }
    r = client.post("/api/lessons", json=payload)
    assert r.status_code == 201
    data = r.get_json()
    assert "id" in data
    lesson_id = data["id"]

    # retrieve list
    r = client.get("/api/lessons/")
    assert r.status_code == 200
    arr = r.get_json()
    assert len(arr) == 1
    assert arr[0]["language"] == "luo"

    # retrieve single
    r = client.get(f"/api/lessons/{lesson_id}")
    assert r.status_code == 200
    assert r.get_json()["episodeTitle"] == "Episode 1"

    # update
    r = client.put(f"/api/lessons/{lesson_id}", json={"difficulty": "medium"})
    assert r.status_code == 200
    r = client.get(f"/api/lessons/{lesson_id}")
    assert r.get_json()["difficulty"] == "medium"

    # delete
    r = client.delete(f"/api/lessons/{lesson_id}")
    assert r.status_code == 200
    r = client.get(f"/api/lessons/{lesson_id}")
    assert r.status_code == 404


def test_question_crud_and_lesson_relation(client):
    # create lesson first
    lesson_payload = {
        "language": "kamba",
        "episodeTitle": "Intro",
        "difficulty": "easy",
        "storyIntro": "Intro story",
        "dialogue": "Hi",
        "exercises": "none",
        "xpReward": 5,
    }
    r = client.post("/api/lessons", json=lesson_payload)
    lesson_id = r.get_json()["id"]

    # create question tied to lesson
    q_payload = {
        "question_type": "fill_in",
        "prompt": "What is 2+2?",
        "answer": "4",
        "lesson_id": lesson_id,
        "xp": 3,
    }
    r = client.post("/api/questions", json=q_payload)
    assert r.status_code == 201
    q_id = r.get_json()["id"]

    # list questions
    r = client.get("/api/questions/")
    assert r.status_code == 200
    assert len(r.get_json()) == 1

    # retrieve by id
    r = client.get(f"/api/questions/{q_id}")
    assert r.status_code == 200
    assert r.get_json()["prompt"] == "What is 2+2?"

    # retrieve by lesson
    r = client.get(f"/api/questions/lesson/{lesson_id}")
    assert r.status_code == 200
    assert len(r.get_json()) == 1

    # update
    r = client.put(f"/api/questions/{q_id}", json={"answer": "four"})
    assert r.status_code == 200
    r = client.get(f"/api/questions/{q_id}")
    assert r.get_json()["answer"] == "four"

    # delete
    r = client.delete(f"/api/questions/{q_id}")
    assert r.status_code == 200
    r = client.get(f"/api/questions/{q_id}")
    assert r.status_code == 404


def test_question_answering_awards_xp_and_lesson_completion_marks_done(client):
    # create user directly in the database
    user = User(
        name="XP Tester",
        email="xp@test.com",
        password_hash=generate_password_hash("password"),
        is_verified=True,
    )
    db.session.add(user)
    db.session.commit()

    # create a lesson
    lesson_payload = {
        "language": "luganda",
        "episodeTitle": "XP Lesson",
        "difficulty": "easy",
        "storyIntro": "XP story",
        "dialogue": "Hello",
        "exercises": "practice",
        "xpReward": 15,
    }
    r = client.post("/api/lessons", json=lesson_payload)
    lesson_id = r.get_json()["id"]

    # create a question tied to that lesson
    question_payload = {
        "question_type": "fill_in",
        "prompt": "What is 2+2?",
        "answer": "4",
        "lesson_id": lesson_id,
        "xp": 5,
    }
    r = client.post("/api/questions", json=question_payload)
    assert r.status_code == 201
    question_id = r.get_json()["id"]

    # wrong answer does not add XP
    r = client.post(
        f"/api/progress/lesson/{lesson_id}/answer",
        json={"user_id": user.id, "question_id": question_id, "answer": "5"},
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data["correct"] is False
    assert data["xpEarned"] == 0
    assert data["totalXp"] == 0

    # correct answer awards XP immediately
    r = client.post(
        f"/api/progress/lesson/{lesson_id}/answer",
        json={"user_id": user.id, "question_id": question_id, "answer": "4"},
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data["correct"] is True
    assert data["xpEarned"] == 5
    assert data["lessonXp"] == 5
    assert data["totalXp"] == 5
    assert data["progress"]["completed"] is False

    # answering the same question again does not award duplicate XP
    r = client.post(
        f"/api/progress/lesson/{lesson_id}/answer",
        json={"user_id": user.id, "question_id": question_id, "answer": "4"},
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data["correct"] is True
    assert data["xpEarned"] == 0
    assert data["lessonXp"] == 5
    assert data["totalXp"] == 5

    # completing the lesson marks it complete without adding extra XP
    r = client.post(f"/api/progress/lesson/{lesson_id}/complete", json={"user_id": user.id})
    assert r.status_code == 200
    data = r.get_json()
    assert data["xpEarned"] == 0
    assert data["lessonXp"] == 5
    assert data["totalXp"] == 5
    assert data["progress"]["completed"] is True

    # second completion still does not add extra XP
    r = client.post(f"/api/progress/lesson/{lesson_id}/complete", json={"user_id": user.id})
    assert r.status_code == 200
    data = r.get_json()
    assert data["xpEarned"] == 0
    assert data["lessonXp"] == 5
    assert data["totalXp"] == 5
