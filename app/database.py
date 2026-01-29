from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER", "user")
password = os.getenv("DB_PASSWORD", "user_pass")
host = os.getenv("DB_HOST", "db")
port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "db_estudiantes")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear sesion (interactuar con la DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()