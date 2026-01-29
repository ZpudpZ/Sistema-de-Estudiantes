from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Datos básicos
class StudentBase(BaseModel):
    codigo: str
    nombres: str
    apellidos: str
    email: EmailStr
    semestre: int

# Datos para crear
class StudentCreate(StudentBase):
    pass

# Datos de respuesta
class StudentResponse(StudentBase):
    id: int
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True