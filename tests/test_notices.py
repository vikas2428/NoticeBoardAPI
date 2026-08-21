from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Running"


def test_get_notices():
    response = client.get("/api/notices")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_notice_analytics():
    response = client.get("/api/notices/analytics")

    assert response.status_code == 200

    data = response.json()

    assert "total_notices" in data
    assert "active_notices" in data
    assert "archived_notices" in data


def test_notice_async_processing():
    response = client.get("/api/notices/async-processing")

    assert response.status_code == 200

    data = response.json()

    assert data["method"] == "asyncio.gather"
    assert "total_processed" in data
    assert "results" in data


def test_notice_processing():
    response = client.get("/api/notices/processing")

    assert response.status_code == 200

    data = response.json()

    assert "iterator_result" in data
    assert "generator_result" in data