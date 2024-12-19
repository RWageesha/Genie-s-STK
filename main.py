# main.py

from data.db_config import engine
from data.models import Base

def main():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    main()
