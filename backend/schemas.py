from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20, description="Código único del estudiante")
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=150)
    semestre: int = Field(..., ge=1, le=14)
    activo: bool = True

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True