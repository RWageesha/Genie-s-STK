# main.py

from data.db_config import engine
from data.models import Base

def main():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully.")

if __name__ == "__main__":
    main()