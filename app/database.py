# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define Settings class to manage environment variables


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "allow"


# Create an instance of Settings
settings = Settings()

# SQLAlchemy setup
# Create a database engine using the DATABASE_URL from settings
engine = create_engine(settings.DATABASE_URL)

# Create a sessionmaker to generate new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define a function to get a database session


def get_db():
    """Return a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Ensure the database connection is closed after use
        db.close()
