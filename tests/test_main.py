from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    # Petición GET (simulado)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "V2 API desplegada automaticamente", "docs": "/docs"}

def test_create_student_validation():
    # Crear un estudiante con datos basura (sin email)
    response = client.post("/estudiantes/", json={
        "codigo": "123",
        "nombres": "Test",
        # Falta el email y apellido a propósito
    })
    # La API debería rechazarlo (código 422 Unprocessable Entity)
    assert response.status_code == 422