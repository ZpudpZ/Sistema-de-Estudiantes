from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
from sqlalchemy.exc import OperationalError
import models, schemas, crud, database

app = FastAPI(title="Sistema de Estudiantes - API")

@app.on_event("startup")
def startup():
    max_retries = 15
    wait_seconds = 5

    for attempt in range(max_retries):
        try:
            print(f"\n[INFO] Intento de conexión a DB: {attempt + 1}/{max_retries}...")
            models.Base.metadata.create_all(bind=database.engine)
            print("[EXITO] Conexión establecida y tablas verificadas.\n")
            break
        except OperationalError as e:
            print(f"[WARN] La base de datos aún no responde. Reintentando en {wait_seconds}s...")
            time.sleep(wait_seconds)
    else:
        print("\n[CRITICO] No se pudo conectar a la DB después de varios intentos.\n")


@app.get("/")
def read_root():
    return {"mensaje": "API de Gestión Académica Operativa", "docs": "/docs"}

@app.post("/estudiantes/", response_model=schemas.StudentResponse)
def crear_estudiante(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=student.codigo)
    if db_student:
        raise HTTPException(status_code=400, detail="El código de matrícula ya existe.")
    return crud.create_student(db=db, student=student)

@app.get("/estudiantes/", response_model=List[schemas.StudentResponse])
def leer_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.get("/estudiantes/buscar/{codigo}", response_model=schemas.StudentResponse)
def leer_estudiante_por_codigo(codigo: str, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=codigo)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@app.get("/estudiantes/{student_id}", response_model=schemas.StudentResponse)
def leer_estudiante_por_id(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@app.put("/estudiantes/{student_id}", response_model=schemas.StudentResponse)
def actualizar_estudiante(student_id: int, student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return crud.update_student(db=db, student_id=student_id, student_data=student)

@app.delete("/estudiantes/{student_id}")
def eliminar_estudiante(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    crud.delete_student(db=db, student_id=student_id)
    return {"mensaje": "Estudiante eliminado correctamente"}