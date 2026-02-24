import sys
import time
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

import models
import schemas
import crud
import database

def init_db():
    max_retries = 15
    wait_seconds = 5
    for attempt in range(max_retries):
        try:
            models.Base.metadata.create_all(bind=database.engine)
            return True
        except OperationalError:
            time.sleep(wait_seconds)
    return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not init_db():
        sys.exit(1)
    yield

app = FastAPI(title="Sistema de Estudiantes - API", lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"status": "online", "service": "academic-management-api"}

@app.post("/estudiantes/", response_model=schemas.StudentResponse, status_code=201)
async def crear_estudiante(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=student.codigo)
    if db_student:
        raise HTTPException(status_code=400, detail="Codigo de matricula duplicado")
    return crud.create_student(db=db, student=student)

@app.get("/estudiantes/", response_model=List[schemas.StudentResponse])
async def leer_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.get("/estudiantes/buscar/{codigo}", response_model=schemas.StudentResponse)
async def leer_estudiante_por_codigo(codigo: str, db: Session = Depends(database.get_db)):
    db_student = crud.get_student_by_code(db, codigo=codigo)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@app.get("/estudiantes/{student_id}", response_model=schemas.StudentResponse)
async def leer_estudiante_por_id(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@app.put("/estudiantes/{student_id}", response_model=schemas.StudentResponse)
async def actualizar_estudiante(student_id: int, student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = crud.update_student(db=db, student_id=student_id, student_data=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@app.delete("/estudiantes/{student_id}", status_code=200)
async def eliminar_estudiante(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    crud.delete_student(db=db, student_id=student_id)
    return {"status": "success", "message": "Record deleted"}