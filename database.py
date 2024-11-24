import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Read environment variables for database configuration
username = os.getenv("DB_USERNAME", "admin")
password = os.getenv("DB_PASSWORD", "group9login")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "3306")
database = os.getenv("DB_NAME", "CCTV_service")

# Database URL
URL_DATABASE = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

# Create engine and session
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()