import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from database import Base, get_db

os.environ["TEST_MODE"] = "True"

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

def test_lectura_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_crear_estudiante_exitoso():
    payload = {
        "codigo": "202601",
        "nombres": "JUAN CARLOS",
        "apellidos": "PEREZ LOPEZ",
        "email": "juan.perez@unap.edu.pe",
        "semestre": 9
    }
    response = client.post("/estudiantes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["codigo"] == "202601"
    assert "id" in data

def test_crear_estudiante_error_validacion():
    response = client.post("/estudiantes/", json={
        "codigo": "123",
        "nombres": "TEST"
    })
    assert response.status_code == 422

def test_crear_estudiante_duplicado():
    payload = {
        "codigo": "202699",
        "nombres": "ANA", "apellidos": "GARCIA", "email": "ana@test.com", "semestre": 1
    }
    client.post("/estudiantes/", json=payload)
    response = client.post("/estudiantes/", json=payload)
    assert response.status_code == 400

def test_lectura_lista_estudiantes():
    client.post("/estudiantes/", json={
        "codigo": "LIST01", "nombres": "A", "apellidos": "B", "email": "a@b.com", "semestre": 1
    })
    response = client.get("/estudiantes/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_flujo_actualizacion_eliminacion():
    res_create = client.post("/estudiantes/", json={
        "codigo": "TEMP01", "nombres": "ORIGINAL", "apellidos": "X", "email": "temp@t.com", "semestre": 1
    })
    student_id = res_create.json()["id"]

    res_update = client.put(f"/estudiantes/{student_id}", json={
        "codigo": "TEMP01", "nombres": "EDITADO", "apellidos": "X", "email": "temp@t.com", "semestre": 2
    })
    assert res_update.status_code == 200
    assert res_update.json()["nombres"] == "EDITADO"

    res_del = client.delete(f"/estudiantes/{student_id}")
    assert res_del.status_code == 200

    res_get = client.get(f"/estudiantes/{student_id}")
    assert res_get.status_code == 404