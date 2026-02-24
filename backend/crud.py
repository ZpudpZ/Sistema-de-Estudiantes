from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import models
import schemas

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_code(db: Session, codigo: str):
    return db.query(models.Student).filter(models.Student.codigo == codigo).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig):
            raise HTTPException(status_code=400, detail="El código o email ya existe.")
        raise HTTPException(status_code=500, detail="Error de integridad.")

def update_student(db: Session, student_id: int, student_data: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    for key, value in student_data.model_dump().items():
        setattr(db_student, key, value)
    
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Conflicto de integridad al actualizar.")

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student