from fastapi.testclient import TestClient

from app.main import app as fastapi_app

client = TestClient(fastapi_app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_path():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}
