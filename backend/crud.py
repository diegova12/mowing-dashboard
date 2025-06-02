# backend/crud.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import your Base so SQLAlchemy knows about models (not strictly needed here, but good practice)
from .models import Base  

# ◼️ Update this URL to match your alembic.ini / Postgres credentials:
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/landscape_db"

# 1) Create the engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,       # optional: checks connections before using
)

# 2) Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 3) Dependency for FastAPI to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
