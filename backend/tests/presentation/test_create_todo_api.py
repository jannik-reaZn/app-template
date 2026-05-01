from uuid import UUID

from fastapi.testclient import TestClient

from main import app
from tests.factory.create_todo_request_factory import CreateTodoRequestFactory

client = TestClient(app)


def test_post_todos_creates_pending_todo() -> None:
    # GIVEN
    payload = CreateTodoRequestFactory.build()

    # WHEN
    response = client.post("/api/todos", json=payload.model_dump())

    # THEN
    assert response.status_code == 201
    response_body = response.json()

    assert UUID(response_body["id"])
    assert response_body == {
        "id": response_body["id"],
        "title": payload.title,
        "status": "pending",
    }


def test_post_todos_rejects_blank_title() -> None:
    # GIVEN
    payload: dict[str, str] = {"title": "   "}

    # WHEN
    response = client.post("/api/todos", json=payload)

    # THEN
    assert response.status_code == 400
    assert response.json() == {"detail": "Todo title cannot be empty"}
