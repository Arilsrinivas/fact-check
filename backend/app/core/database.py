from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

# Fallback to SQLite if no DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourcetrace.db")

# Use NullPool with SQLite to avoid "database is locked" and unclosed resource warnings during dev reload
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    poolclass=NullPool if "sqlite" in DATABASE_URL else None
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
