# test_connection.py

import psycopg2
from psycopg2 import OperationalError

def test_connection(url):
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("PostgreSQL Database Version:", db_version)
        cursor.close()
        conn.close()
        return True
    except OperationalError as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    connection_url = "postgresql://postgres:pass@localhost:5432/pharmacy_db"
    if test_connection(connection_url):
        print("PostgreSQL is working and accessible.")
    else:
        print("Failed to connect to PostgreSQL.")
