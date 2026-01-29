from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, database

app = FastAPI(title="Sistema de Estudiantes - Pruebas CI/CD")

@app.on_event("startup")
def startup():
    # Intento de conexion (60 seg)
    max_retries = 12
    wait_seconds = 5
    
    for attempt in range(max_retries):
        try:
            print(f"--- Intento de conexión a DB: {attempt + 1}/{max_retries} ---")
            models.Base.metadata.create_all(bind=database.engine)
            print("--- ¡CONEXIÓN EXITOSA! Tablas creadas/verificadas ---")
            break
        except OperationalError as e:
            print(f"--- La base de datos aún no está lista. Reintentando en {wait_seconds}s... ---")
            print(f"Detalle: {e}")
            time.sleep(wait_seconds)
    else:
        print("--- ERROR: No se pudo conectar a la DB después de varios intentos ---")

@app.get("/")
def read_root():
    return {"mensaje": "V2 API desplegada automaticamente", "docs": "/docs"}

@app.post("/estudiantes/", response_model=schemas.StudentResponse)
def crear_estudiante(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=student.codigo)
    if db_student:
        raise HTTPException(status_code=400, detail="El código ya existe")
    return crud.create_student(db=db, student=student)

@app.get("/estudiantes/", response_model=List[schemas.StudentResponse])
def leer_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_students(db, skip=skip, limit=limit)
