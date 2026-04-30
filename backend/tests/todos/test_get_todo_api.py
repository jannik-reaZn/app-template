from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_todo_returns_existing_todo() -> None:
    created_response = client.post("/api/todos", json={"title": "Pay electricity bill"})

    todo_id = created_response.json()["id"]
    response = client.get(f"/api/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": todo_id,
        "title": "Pay electricity bill",
        "status": "pending",
    }


def test_get_todo_returns_not_found_for_missing_id() -> None:
    response = client.get("/api/todos/missing-todo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
