from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import Base

DATABASE_URL = "postgresql://postgres:pass@localhost:5432/pharmacy_db"

engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db():

    """
    Initialize the database by dropping all tables and recreating them.
    **WARNING:** This will delete all existing data.
    """
   # Base.metadata.drop_all(bind=engine)
    #Base.metadata.create_all(bind=engine)



    Base.metadata.create_all(bind=engine)
    
