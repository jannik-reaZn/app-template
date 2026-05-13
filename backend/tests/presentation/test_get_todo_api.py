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
        "tags": [],
    }


def test_get_todo_returns_existing_todo_with_notes() -> None:
    # GIVEN
    payload = CreateTodoRequestFactory.build(
        title="Buy groceries",
        notes=["Buy oat milk", "Check pantry first"],
    )
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
        "notes": payload.notes,
        "tags": [],
    }


def test_get_todo_returns_existing_todo_with_tags() -> None:
    # GIVEN
    payload = CreateTodoRequestFactory.build(
        title="Buy groceries",
        tags=["groceries", "weekly"],
    )
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
        "tags": payload.tags,
    }


def test_get_todo_returns_not_found_for_missing_id() -> None:
    # GIVEN
    missing_todo_id: str = "missing-todo"

    # WHEN
    response = client.get(f"/api/todos/{missing_todo_id}")

    # THEN
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoEntity not found"}


def test_delete_todo_removes_existing_todo() -> None:
    # GIVEN
    payload = CreateTodoRequestFactory.build()
    created_response = client.post("/api/todos", json=payload.model_dump())

    # WHEN
    todo_id = created_response.json()["id"]
    delete_response = client.delete(f"/api/todos/{todo_id}")
    get_response = client.get(f"/api/todos/{todo_id}")

    # THEN
    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404


def test_delete_todo_returns_not_found_for_missing_id() -> None:
    # GIVEN
    missing_todo_id = "missing-todo"

    # WHEN
    response = client.delete(f"/api/todos/{missing_todo_id}")

    # THEN
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoEntity not found"}
