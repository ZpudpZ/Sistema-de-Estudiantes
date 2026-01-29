from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time

from . import models, schemas, crud, database

time.sleep(10)

# Crear las tablas en MySQL
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sistema de Estudiantes - Pruebas CI/CD")

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente", "docs": "/docs"}

@app.post("/estudiantes/", response_model=schemas.StudentResponse)
def crear_estudiante(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=student.codigo)
    if db_student:
        raise HTTPException(status_code=400, detail="El código ya existe")
    return crud.create_student(db=db, student=student)

@app.get("/estudiantes/", response_model=List[schemas.StudentResponse])
def leer_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_students(db, skip=skip, limit=limit)