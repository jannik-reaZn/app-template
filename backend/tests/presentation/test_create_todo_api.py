from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_post_todos_creates_pending_todo() -> None:
    response = client.post("/api/todos", json={"title": "Pay electricity bill"})

    assert response.status_code == 201
    assert response.json() == {
        "id": "todo-1",
        "title": "Pay electricity bill",
        "status": "pending",
    }


def test_post_todos_rejects_blank_title() -> None:
    response = client.post("/api/todos", json={"title": "   "})

    assert response.status_code == 400
    assert response.json() == {"detail": "Todo title cannot be empty"}
