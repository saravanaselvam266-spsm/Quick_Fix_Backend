import sys
from sqlalchemy import create_engine, text
from db.database import DB_URL

print(f"Testing connection to: {DB_URL}")

try:
    engine = create_engine(DB_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection Successful!", result.scalar())
except Exception as e:
    print(f"Connection Failed: {e}")
    sys.exit(1)
