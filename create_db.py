import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Config from database.py (hardcoded for now as per that file)
username = "postgres"
password = "AcademyRootPassword"
hostname = "localhost"
port = "5432"
new_db_name = "db_for_project"

def create_database():
    try:
        # Connect to default 'postgres' database to create a new one
        con = psycopg2.connect(
            user=username, 
            password=password, 
            host=hostname, 
            port=port, 
            dbname="postgres"
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        
        # Check if exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE dataname = '{new_db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {new_db_name}...")
            cursor.execute(f"CREATE DATABASE {new_db_name}")
            print("Database created successfully!")
        else:
            print(f"Database {new_db_name} already exists.")
            
        cursor.close()
        con.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

if __name__ == "__main__":
    create_database()
