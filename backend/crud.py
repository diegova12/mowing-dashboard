# backend/crud.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base  

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/landscape_db"

# Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Dependency for FastAPI to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
