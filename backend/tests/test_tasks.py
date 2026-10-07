from fastapi.testclient import TestClient

from app.main import app


def test_blank_title_is_rejected():
    with TestClient(app) as client:
        response = client.post("/tasks", json={"title": "   "})
        assert response.status_code == 422


def test_task_lifecycle():
    with TestClient(app) as client:
        response = client.post(
            "/tasks",
            json={"title": "Temporary automated test task"},
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        try:
            assert response.json()["status"] == "todo"

            response = client.patch(
                f"/tasks/{task_id}",
                json={"status": "in_progress"},
            )
            assert response.status_code == 200
            assert response.json()["status"] == "in_progress"

            response = client.patch(
                f"/tasks/{task_id}",
                json={"status": "invalid"},
            )
            assert response.status_code == 422

            response = client.delete(f"/tasks/{task_id}")
            assert response.status_code == 204

            response = client.patch(
                f"/tasks/{task_id}",
                json={"status": "done"},
            )
            assert response.status_code == 404
        finally:
            client.delete(f"/tasks/{task_id}")
