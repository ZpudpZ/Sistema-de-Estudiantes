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

# Actualizar estudiante
def update_student(db: Session, student_id: int, student_data: schemas.StudentBase):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db_student.codigo = student_data.codigo
        db_student.nombres = student_data.nombres
        db_student.apellidos = student_data.apellidos
        db_student.email = student_data.email
        db_student.semestre = student_data.semestre
        db.commit()
        db.refresh(db_student)
    return db_student

# Borrar estudiante
def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student