from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os


# Helper to read .env file manually since python-dotenv is causing issues
def load_env_file(filepath=".env"):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                os.environ[key.strip()] = value


load_env_file()

DB_URL = os.getenv("DATABASE_URL")

# SQLAlchemy requires 'postgresql://', but some providers give 'postgres://'
if DB_URL and DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
