from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
import os

# Database Configuration
# ==============================
# SQLite Configuration (Default)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./candidates.db")

# For PostgreSQL, use:
# DATABASE_URL = "postgresql://user:password@localhost:5432/resume_db"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL query logging
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session for FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Call this function once during application startup.
    """
    Base.metadata.create_all(bind=engine)