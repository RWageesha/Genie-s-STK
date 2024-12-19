# data/db_config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:123@localhost:5432/pharmacy_db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    """
    Initialize the database by dropping all tables and recreating them.
    **WARNING:** This will delete all existing data.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise e


#"postgresql://postgres:pass@localhost:5432/pharmacy_db"