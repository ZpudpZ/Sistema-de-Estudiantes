from sqlalchemy.orm import Session
from . import models, schemas

# Buscar por ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Buscar por Código
def get_student_by_code(db: Session, codigo: str):
    return db.query(models.Student).filter(models.Student.codigo == codigo).first()

# Listar todos
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

# Crear nuevo
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        codigo=student.codigo,
        nombres=student.nombres,
        apellidos=student.apellidos,
        email=student.email,
        semestre=student.semestre
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student