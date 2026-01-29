from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

TEST_MODE = os.getenv("TEST_MODE", "").lower() in ["true", "1", "yes"]

if TEST_MODE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    connect_args = {"check_same_thread": False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
else:
    user = os.getenv("DB_USER", "user")
    password = os.getenv("DB_PASSWORD", "user_pass")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "db_estudiantes")

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()