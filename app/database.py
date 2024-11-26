import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Read environment variables for database configuration
username = "admin"
password = "amogus"
host = "localhost:3306"
database = "CCTV_service"

# Database URL
URL_DATABASE = f"mysql+pymysql://{username}:{password}@{host}/{database}"

# Create engine and session
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()