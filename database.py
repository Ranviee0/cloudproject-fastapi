from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define connection details
username = "admin"
password = "group9login"
host = "localhost"
port = 3307
database = "new_schema"

URL_DATABASE = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()