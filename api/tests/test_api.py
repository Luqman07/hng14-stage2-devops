import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import main  # your FastAPI file

client = TestClient(main.app)


@pytest.fixture
def mock_redis(monkeypatch):
    mock = MagicMock()

    # Mock Redis behavior
    mock.lpush.return_value = 1
    mock.hset.return_value = True
    mock.hget.return_value = "queued"

    # Replace the Redis instance in your app
    monkeypatch.setattr(main, "r", mock)

    return mock


def test_create_job(mock_redis):
    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()

    assert "job_id" in data
    assert isinstance(data["job_id"], str)

    # Ensure Redis was called
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


def test_get_job_success(mock_redis):
    response = client.get("/jobs/test-id")

    assert response.status_code == 200
    data = response.json()

    assert data["job_id"] == "test-id"
    assert data["status"] == "queued"


def test_get_job_not_found(monkeypatch):
    mock = MagicMock()
    mock.hget.return_value = None

    monkeypatch.setattr(main, "r", mock)

    response = client.get("/jobs/unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"