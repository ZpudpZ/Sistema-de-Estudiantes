from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

def read_secret(secret_name):
    path = f'/run/secrets/{secret_name}'
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None
    except Exception as e:
        print(f"Error leyendo secreto {secret_name}: {e}")
        return None

load_dotenv()

if os.getenv("TEST_MODE") == "True":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    user = read_secret("db_user") or os.getenv("DB_USER")
    password = read_secret("db_password") or os.getenv("DB_PASSWORD")
    db_name = read_secret("db_name") or os.getenv("DB_NAME")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "3306")

    if not all([user, password, db_name]):
        raise RuntimeError("Faltan credenciales críticas para la base de datos.")

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        pool_recycle=3600,
        pool_pre_ping=True 
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()