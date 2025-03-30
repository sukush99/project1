""" Lets configure the database connection"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from loguru import logger

# SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"

try:
    # Create the database engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a base class for declarative models
    Base = declarative_base()
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error(f"Error connecting to the database: {e}")
    raise