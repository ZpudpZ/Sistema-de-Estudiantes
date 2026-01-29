import os

os.environ["TEST_MODE"] = "True"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "V2 API desplegada automaticamente",
        "docs": "/docs"
    }


def test_create_student_validation():
    response = client.post("/estudiantes/", json={
        "codigo": "123",
        "nombres": "Test"
    })
    assert response.status_code == 422
