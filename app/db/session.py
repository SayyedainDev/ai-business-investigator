import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set! Check your .env file.")

# The Engine is the starting point for any SQLAlchemy application.
# It acts as a central registry for the database connection pool.
engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal is a factory that generates new database sessions for our API requests.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all our future ORM models.
Base = declarative_base()

def get_db():
    """
    Dependency generator for FastAPI.
    Yields a database session and safely closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()