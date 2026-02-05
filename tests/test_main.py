import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["TEST_MODE"] = "True"

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "V2 API desplegada automaticamente",
        "docs": "/docs"
    }

def test_create_student_success():
    payload = {
        "codigo": "2024-100",
        "nombres": "Wilder",
        "apellidos": "Ingeniero",
        "email": "wilder@oti.com",
        "semestre": 9
    }
    response = client.post("/estudiantes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["codigo"] == "2024-100"
    assert "id" in data

def test_create_student_validation_error():
    response = client.post("/estudiantes/", json={
        "codigo": "123",
        "nombres": "Test"
    })
    assert response.status_code == 422

def test_create_student_duplicate_error():
    payload = {
        "codigo": "DUPLICADO",
        "nombres": "A", "apellidos": "B", "email": "a@b.com", "semestre": 1
    }
    client.post("/estudiantes/", json=payload)
    
    response = client.post("/estudiantes/", json=payload)
    assert response.status_code == 400
    assert "El código ya existe" in response.json()["detail"]

def test_read_students_list():
    client.post("/estudiantes/", json={
        "codigo": "LIST-01", "nombres": "N", "apellidos": "A", "email": "l@l.com", "semestre": 1
    })
    response = client.get("/estudiantes/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_and_delete_flow():
    res_create = client.post("/estudiantes/", json={
        "codigo": "TEMP-01", "nombres": "Original", "apellidos": "X", "email": "t@t.com", "semestre": 1
    })
    student_id = res_create.json()["id"]

    res_update = client.put(f"/estudiantes/{student_id}", json={
        "codigo": "TEMP-01", "nombres": "Editado", "apellidos": "X", "email": "t@t.com", "semestre": 2
    })
    assert res_update.status_code == 200
    assert res_update.json()["nombres"] == "Editado"

    res_del = client.delete(f"/estudiantes/{student_id}")
    assert res_del.status_code == 200

    res_get = client.get(f"/estudiantes/{student_id}")
    assert res_get.status_code == 404