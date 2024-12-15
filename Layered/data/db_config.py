from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import Base

DATABASE_URL = "postgresql://username:password@localhost:5432/pharmacy_db"

engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)
