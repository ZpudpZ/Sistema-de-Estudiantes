from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos de estudiante
    codigo = Column(String(20), unique=True, index=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    semestre = Column(Integer, nullable=False)
    
    # Datos de control
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())