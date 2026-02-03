from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

def read_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r', encoding='utf-8-sig') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return None

load_dotenv()

if os.getenv("TEST_MODE") == "True":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    connect_args = {"check_same_thread": False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
    print("\nMODO TEST: Usando SQLite\n")

else:
    user = read_secret("db_user")
    password = read_secret("db_password")
    db_name = read_secret("db_name")
    
    if not user:
        user = os.getenv("DB_USER", "user")
    if not password:
        password = os.getenv("DB_PASSWORD", "user_pass")
    if not db_name:
        db_name = os.getenv("DB_NAME", "db_estudiantes")

    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "3306")
    
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
    print("\nMODO PRODUCCIÓN: Usando MySQL\n")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()