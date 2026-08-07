import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ==================================
# LOAD ENV
# ==================================

load_dotenv()

# ==================================
# DATABASE URL
# ==================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL belum diatur pada Environment Variables."
    )

# ==================================
# ENGINE
# ==================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# ==================================
# SESSION
# ==================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==================================
# BASE
# ==================================

Base = declarative_base()

# ==================================
# GET DB
# ==================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()