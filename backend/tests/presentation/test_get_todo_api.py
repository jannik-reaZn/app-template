from fastapi.testclient import TestClient

from main import app
from tests.factory.create_todo_request_factory import CreateTodoRequestFactory

client = TestClient(app)


def test_get_todo_returns_existing_todo() -> None:
    # GIVEN
    payload = CreateTodoRequestFactory.build()
    created_response = client.post("/api/todos", json=payload.model_dump())

    # WHEN
    todo_id = created_response.json()["id"]
    response = client.get(f"/api/todos/{todo_id}")

    # THEN
    assert response.status_code == 200
    assert response.json() == {
        "id": todo_id,
        "title": payload.title,
        "status": "pending",
        "notes": [],
    }


def test_get_todo_returns_existing_todo_with_notes() -> None:
    # GIVEN
    payload: dict[str, object] = {
        "title": "Buy groceries",
        "notes": ["Buy oat milk", "Check pantry first"],
    }
    created_response = client.post("/api/todos", json=payload)

    # WHEN
    todo_id = created_response.json()["id"]
    response = client.get(f"/api/todos/{todo_id}")

    # THEN
    assert response.status_code == 200
    assert response.json() == {
        "id": todo_id,
        "title": "Buy groceries",
        "status": "pending",
        "notes": ["Buy oat milk", "Check pantry first"],
    }


def test_get_todo_returns_not_found_for_missing_id() -> None:
    # GIVEN
    missing_todo_id: str = "missing-todo"

    # WHEN
    response = client.get(f"/api/todos/{missing_todo_id}")

    # THEN
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoEntity not found"}
